from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from webob import Response
import json

class FlowAnalyzer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    _CONTEXTS = {
        'wsgi': WSGIApplication
    }

    def __init__(self, *args, **kwargs):
        super(FlowAnalyzer, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.flow_stats = defaultdict(list)
        self.catboost_model = joblib.load('catboost_model.pkl')  # Load the pre-trained CatBoost model
        self.valid_ip_ranges = ['192.168.0.0/16']  # Default valid IP ranges

        wsgi = kwargs['wsgi']
        wsgi.register(FlowAnalyzerController, {'flow_analyzer': self})

    # Existing methods...

    def set_valid_ip_ranges(self, ip_ranges):
        self.valid_ip_ranges = ip_ranges

class FlowAnalyzerController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(FlowAnalyzerController, self).__init__(req, link, data, **config)
        self.flow_analyzer = data['flow_analyzer']

    @route('flowanalyzer', '/valid_ip_ranges', methods=['POST'])
    def update_valid_ip_ranges(self, req, **kwargs):
        try:
            new_ip_ranges = json.loads(req.body.decode('utf-8'))
            self.flow_analyzer.set_valid_ip_ranges(new_ip_ranges)
            return Response(status=200, body=json.dumps({'status': 'success'}))
        except Exception as e:
            return Response(status=500, body=json.dumps({'status': 'error', 'message': str(e)}))

# Ryu command to run the application
if __name__ == '__main__':
    app_manager.run_apps([FlowAnalyzer])
