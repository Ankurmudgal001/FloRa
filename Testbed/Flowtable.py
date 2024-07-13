from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub

class SetFlowTableSize(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SetFlowTableSize, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        self.datapaths[datapath.id] = datapath
        self._set_flow_table_size(datapath)

    def _set_flow_table_size(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPTableMod(datapath, table_id=0, config=ofproto.OFPTC_DEPRECATED_MASK, max_entries=1500)
        datapath.send_msg(req)
        self.logger.info("Set flow table size to 1500 entries for datapath: %016x", datapath.id)

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._set_flow_table_size(dp)
            hub.sleep(10)

    @set_ev_cls(ofp_event.EventOFPStateChange, [CONFIG_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == CONFIG_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info('Register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
                self._set_flow_table_size(datapath)
        elif ev.state == 'DEAD_DISPATCHER':
            if datapath.id in self.datapaths:
                self.logger.info('Unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

if __name__ == '__main__':
    app_manager.run_apps([SetFlowTableSize])
