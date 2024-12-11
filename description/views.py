from django.shortcuts import render, redirect
import paramiko
import environ
import re
import netmiko
import json
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
from ntc_templates.parse import parse_output
from django.http import HttpResponse
import os
import textfsm
import textfsm.parser



env = environ.Env()

device_type = env(str('DEVICE_TYPE'))
hostname = env(str('HOST_NAME'))
username = env(str('USER_NAME'))
password = env(str('PASSWORD'))




def check_env_variable(request):
    net_textfsm = os.environ.get('NET_TEXTFSM', 'Not set')
    return HttpResponse(f'NET_TEXTFSM: {net_textfsm}')



def show_description(request):
    
    context = {}
    
    if request.method == 'POST':
        try:
            # Define the device connection details
            device = {
                'device_type':device_type, # Cisco router or switch version
                'host':hostname,       
                'username':username, 
                'password':password,
            }
            net_connect = ConnectHandler(**device)
            
            if "interface_description" in request.POST:
                button_name = "interface_description"
                command = env(str('SHOW_INTERFACE_DESCRIPTION'))
                
            elif "interface_brief" in request.POST:
                button_name = "interface_brief"
                command = env(str('SHOW_INTERFACE_BRIEF'))
                
            elif "device_version" in request.POST:
                button_name = "device_version"
                command = env(str('SHOW_VERSION'))
                
            elif "ip_interface" in request.POST:
                button_name = "ip_interface"
                command = env(str('SHOW_IP_INTERFACE'))
                
            elif "policy_map_details" in request.POST:
                button_name = "policy_map_details"
                command = env(str('SHOW_RUN_POLICY_MAP'))
                
            elif "running_configuration" in request.POST:
                button_name = "running_configuration"
                command = env(str('SHOW_RUN'))
                
            elif "ip_route" in request.POST:
                button_name = "ip_route"
                command = env(str('SHOW_IP_ROUTE'))
                
            elif "all_interface" in request.POST:
                button_name = "all_interface"
                command = env(str('SHOW_INTERFACES'))
                
            elif "process_cpu" in request.POST:
                button_name = "process_cpu"
                command = env(str('SHOW_PROCESS_CPU'))
            
            elif "memory_summary" in request.POST:
                button_name = "memory_summary"
                command = env(str('SHOW_MEMORY_SUMMARY'))
            
            
            
            
            # for testing
            elif "test" in request.POST:
                button_name = "test"
                
                # Send the show run policy-map command
                output = net_connect.send_command('show memory summary')
                print("raw", output)
                
                # Specify the template path if it's not in the default location
                template_path = 'D:/projects/inception/env/Lib/site-packages/ntc_templates/templates/cisco_xr_show_memory_summary.textfsm'
                with open(template_path, 'r') as template:
                    fsm = textfsm.TextFSM(template)
                # Parse the output using your custom template
                parsed_output = fsm.ParseText(text=output)

                print("parsed", parsed_output)
                command = ""


            command_output = net_connect.send_command(command, use_textfsm=True)
            net_connect.disconnect()
            
            context = {
                "data":command_output,
                "data_type":type(command_output),
                "clicked_button_name":button_name
            }

            return render(request, 'description/get-description.html', context)
        
        except NetmikoTimeoutException:
            print("Connection timed out.")
        except NetmikoAuthenticationException:
            print("Authentication failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    return render(request, 'description/get-description.html', context)