from nornir import InitNornir
from nornir.plugins.tasks.networking import netconf_edit_config
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.data import load_yaml
from nornir.plugins.tasks.text import template_file

nr = InitNornir(config_file="config.yaml")

def load_vars(task):
    data = task.run(task=load_yaml,file=f'./host_vars/{task.host}.yaml')
    task.host["facts"] = data.result
    config_ntp(task)


def config_ntp(task):
    ntp_template = task.run(task=template_file,name="Buildling NTP Configuration",template="ntp.j2", path="./templates")
    ntp_output = ntp_template.result
    task.run(task=netconf_edit_config, target="running", config=ntp_output)


result=nr.run(task=load_vars)
print_result(result)
