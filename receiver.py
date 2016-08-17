"""receiver modul"""

import datetime
import xml.etree.ElementTree
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import model

class OpennmsReceiver(object):
    """Receiver for OpenNMS alarms"""

    def __init__(self, config):
        self.__config = config

    def get_alarms(self):
        """Get all alarms from OpenNMS and return a list with
        model.ActiveAlarm objects
        """
        alarms = []

        # config
        config_rest_url = "https://demo.opennms.org/opennms/rest"
        config_rest_user = "demo"
        config_rest_pw = "demo"

        # get alarms from OpenNMS REST API
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        request_url = config_rest_url + "/alarms?limit=0"
        try:
            response = requests.get(request_url, auth=(config_rest_user, config_rest_pw),
                                    verify=False)
        except:
            raise
        if response.status_code != 200:
            raise Exception("Error connecting to OpenNMS: HTTP/" + str(response.status_code))

        # parse xml and create alarm
        xml_tree = xml.etree.ElementTree.fromstring(response.text)
        for alarm in xml_tree.findall("./alarm"):
            alarm_id = alarm.attrib["id"]
            alarm_severity = alarm.attrib["severity"]
            alarm_logmsg = None
            alarm_description = None
            alarm_uei = None
            alarm_nodelabel = None
            alarm_interface = None
            alarm_service = None
            alarm_operinstruct = None
            alarm_timestamp = None
            for logmessage in alarm.findall("./logMessage"):
                alarm_logmsg = logmessage.text
            for description in alarm.findall("./description"):
                alarm_description = description.text
            for uei in alarm.findall("./uei"):
                alarm_uei = uei.text
            for node in alarm.findall("./nodeLabel"):
                alarm_nodelabel = node.text
            for ipaddress in alarm.findall("./ipAddress"):
                alarm_interface = ipaddress.text
            for service in alarm.findall("./service"):
                alarm_service = service.text
            for operinstruct in alarm.findall("./operinstruct"):
                alarm_operinstruct = operinstruct.text
            for timestamp in alarm.findall("./firstEventTime"):
                # parse date example 2016-08-15T15:00:03.208-04:00
                # ignore timezone
                alarm_timestamp = datetime.datetime.strptime(timestamp.text[:-6],
                                                             "%Y-%m-%dT%H:%M:%S.%f")


            # create alarm
            created_alarm = model.ActiveAlarm(
                alarm_id=alarm_id,
                alarm_uei=alarm_uei,
                alarm_timestamp=alarm_timestamp,
                alarm_severity=alarm_severity,
                alarm_node_label=alarm_nodelabel,
                alarm_node_interface=alarm_interface,
                alarm_node_service=alarm_service,
                alarm_logmsg=alarm_logmsg,
                alarm_description=alarm_description,
                alarm_operinstruct=alarm_operinstruct
            )
            alarms.append(created_alarm)

        # return alarm list
        return alarms
