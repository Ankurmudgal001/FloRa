from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
import random
import time

class MonitorAgent(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MonitorAgent, self).__init__(*args, **kwargs)
        self.threshold = 0.7  # Utilization threshold for detecting attack
        self.detection_window = 5  # Window size to observe utilization trend
        self.utilization_history = {}  # Dictionary to store utilization history per datapath

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        self.utilization_history[datapath.id] = []
        self.install_default_flow(datapath)

    def install_default_flow(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, match, actions)

    def add_flow(self, datapath, match, actions, idle_timeout=0, hard_timeout=0):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        flow_mod = parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=idle_timeout,
            hard_timeout=hard_timeout, priority=0, instructions=instructions
        )
        datapath.send_msg(flow_mod)

    def monitor_utilization(self, datapath, current_utilization):
        if datapath.id in self.utilization_history:
            self.utilization_history[datapath.id].append(current_utilization)

            if len(self.utilization_history[datapath.id]) > self.detection_window:
                trend_window = self.utilization_history[datapath.id][-self.detection_window:]
                avg_utilization = sum(trend_window) / self.detection_window
                if avg_utilization > self.threshold:
                    return True  # Potential attack detected
        return False

class VigilantFlowRuleManager(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(VigilantFlowRuleManager, self).__init__(*args, **kwargs)
        self.cache_region = {}
        self.pending_region = {}
        self.confirmed_region = {}

    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        flow_id = msg.cookie

        if flow_id in self.pending_region[datapath.id]:
            self.confirm_flow(datapath, flow_id)
        elif flow_id in self.confirmed_region[datapath.id]:
            del self.confirmed_region[datapath.id][flow_id]

    def confirm_flow(self, datapath, flow_id):
        self.confirmed_region.setdefault(datapath.id, {})[flow_id] = True
        del self.pending_region[datapath.id][flow_id]

    def handle_detected_attack(self, datapath):
        # Example: move all pending flows to confirmed region
        self.confirmed_region.setdefault(datapath.id, {}).update(self.pending_region.get(datapath.id, {}))
        self.pending_region[datapath.id] = {}

class MaliciousFlowHandler(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MaliciousFlowHandler, self).__init__(*args, **kwargs)
        self.blacklist = {}

    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        flow_id = msg.cookie

        if flow_id in self.blacklist.get(datapath.id, {}):
            del self.blacklist[datapath.id][flow_id]

    def update_blacklist(self, datapath, malicious_flows):
        self.blacklist.setdefault(datapath.id, {}).update({flow_id: True for flow_id in malicious_flows})

    def filter_packet_in_messages(self, datapath, flow_id):
        if flow_id in self.blacklist.get(datapath.id, {}):
            print(f"Dropped packet-in message from malicious flow: {flow_id}")
            return False  # Drop message for malicious flow
        else:
            print(f"Delivered packet-in message for flow: {flow_id}")
            return True  # Allow message for benign flow

if __name__ == '__main__':
    from ryu import cfg

    CONF = cfg.CONF
    CONF.register_cli_opts([
        cfg.StrOpt('mode', default='normal',
                   choices=['normal', 'attacker'],
                   help='execution mode')
    ])

    app_manager.main()
