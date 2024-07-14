from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types
import numpy as np
from collections import defaultdict
import time
from math import log2
from catboost import CatBoostClassifier
import joblib
from scapy.all import IP

class FloRa(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FloRa, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.flow_stats = defaultdict(list)
        self.catboost_model = joblib.load('catboost_model.pkl')  # Load the pre-trained CatBoost model
        self.valid_ip_ranges = ['192.168.0.0/16']  # Default valid IP ranges

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, CONFIG_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            self.logger.info('Register datapath: %016x', datapath.id)
            self.datapaths[datapath.id] = datapath
        elif ev.state == 'DEAD_DISPATCHER':
            if datapath.id in self.datapaths:
                self.logger.info('Unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Request flow stats
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        body = ev.msg.body

        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'], flow.match['eth_dst'])):
            self.flow_stats[stat.match['eth_src']].append(stat)
        
        for eth_src, stats in self.flow_stats.items():
            PAF = self.calculate_packet_arrival_frequency(stats)
            CRS = self.calculate_CRS(stats)
            PSI = self.check_spoofed_ip(stats)
            Mean_duration, CVD = self.calculate_mean_and_cv([s.duration_sec for s in stats])
            Mean_packets, CVP = self.calculate_mean_and_cv([s.packet_count for s in stats])
            Mean_bytes, CVB = self.calculate_mean_and_cv([s.byte_count for s in stats])

           features = [
                Duration, N_Packets, N_Btytes, Mean_Duration, Mean_Packets, Mean_Bytes,
		CVD, CVP, CVB, PAF, PSI, CRS ]


            anomaly_detected = self.catboost_model.predict([features])
            if anomaly_detected:
                self.logger.info('Anomaly detected for source: %s', eth_src)

    def calculate_packet_arrival_frequency(self, stats):
        if len(stats) < 2:
            return 0
        timestamps = [s.duration_nsec for s in stats]
        time_diffs = np.diff(sorted(timestamps))
        frequency = 1 / np.mean(time_diffs) if np.mean(time_diffs) != 0 else 0
        return frequency

    def calculate_entropy(self, values):
        total_count = len(values)
        value_counts = defaultdict(int)
        for value in values:
            value_counts[value] += 1
        entropy = -sum((count / total_count) * log2(count / total_count) for count in value_counts.values())
        return entropy

    def calculate_CRS(self, stats):
        total_entropy = self.calculate_entropy([s.match['eth_src'] for s in stats])
        conditional_entropy = 0
        for s in stats:
            conditional_entropy += (s.packet_count / sum(s.packet_count for s in stats)) * self.calculate_entropy([s.match['eth_src']])
        information_gain = total_entropy - conditional_entropy
        return information_gain

    def check_spoofed_ip(self, stats):
        for s in stats:
            if not self.is_valid_ip(s.match['ipv4_src']):
                return 1
        return 0

    def is_valid_ip(self, ip):
        for valid_range in self.valid_ip_ranges:
            if IP(ip) in IP(valid_range):
                return True
        return False

    def calculate_mean_and_cv(self, values):
        mean = np.mean(values)
        cv = np.std(values) / mean if mean != 0 else 0
        return mean, cv
