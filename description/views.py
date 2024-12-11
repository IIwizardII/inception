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




def create_sub_interface(request):
    try:
        # Define the device connection details
        device = {
            'device_type':device_type,
            'host':hostname,       
            'username':username, 
            'password':password,
        }
        net_connect = ConnectHandler(**device)
        command = env(str('SHOW_INTERFACE_CONFIG'))
        command_output = net_connect.send_command(command, use_textfsm=True)
        
        net_connect.disconnect()
        
        context = {
            "data":command_output,
            "data_type":type(command_output),
        }
        
        return render(request, "description/interface-config.html", context)
    
    except NetmikoTimeoutException:
            print("Connection timed out.")
    except NetmikoAuthenticationException:
        print("Authentication failed.")
    except Exception as e:
        print(f"An error occurred: {e}")



def change_bandwidth(request):
    pass




# accessing a interface
def interface_config(request, value):
    
    context = {}
    
    try:
        # Define the device connection details
        device = {
            'device_type':device_type,
            'host':hostname,       
            'username':username, 
            'password':password,
        }
        net_connect = ConnectHandler(**device)
        command = env(str('SHOW_INTERFACE_CONFIG'))
        command = command.replace("INTERFACE-NAME", value)
        command_output = net_connect.send_command(command, use_textfsm=True)
        
        net_connect.disconnect()
        
        context = {
            "data":command_output,
            "data_type":type(command_output),
            "interface_name":value
        }
        
        return render(request, "description/interface-config.html", context)
    
    except NetmikoTimeoutException:
            print("Connection timed out.")
    except NetmikoAuthenticationException:
        print("Authentication failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
    return render(request, "description/interface-config.html", context)





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
            
            elif "directory" in request.POST:
                button_name = "directory"
                command = env(str('DIRECTORY'))
                
            elif "show_arp" in request.POST:
                button_name = "show_arp"
                command = env(str('SHOW_ARP'))
            
            elif "show_bgp" in request.POST:
                button_name = "show_bgp"
                command = env(str('SHOW_BGP'))
            
            elif "show_bgp_instance_summary" in request.POST:
                button_name = "show_bgp_instance_summary"
                command = env(str('SHOW_BGP_INSTANCE_SUMMARY'))
            
            elif "show_bgp_neighbors" in request.POST:
                button_name = "show_bgp_neighbors"
                command = env(str('SHOW_BGP_NEIGHBORS'))
            
            elif "show_configuration_commit_list" in request.POST:
                button_name = "show_configuration_commit_list"
                command = env(str('SHOW_CONFIGURATION_COMMIT_LIST'))
            
            elif "show_ip_bgp_summary" in request.POST:
                button_name = "show_ip_bgp_summary"
                command = env(str('SHOW_IP_BGP_SUMMARY'))
            
            elif "show_ipv4_interface" in request.POST:
                button_name = "show_ipv4_interface"
                command = env(str('SHOW_IPV4_INTERFACE'))
            
            elif "show_ipv4_vrf_interface_brief" in request.POST:
                button_name = "show_ipv4_vrf_interface_brief"
                command = env(str('SHOW_IPV4_VRF_INTERFACE_BRIEF'))
            
            elif "show_ipv6_neighbors" in request.POST:
                button_name = "show_ipv6_neighbors"
                command = env(str('SHOW_IPV6_NEIGHBORS'))
            
            elif "show_isis_neighbors" in request.POST:
                button_name = "show_isis_neighbors"
                command = env(str('SHOW_ISIS_NEIGHBORS'))
            
            elif "show_vrf_detail" in request.POST:
                button_name = "show_vrf_detail"
                command = env(str('SHOW_VRF_DETAIL'))
            
            elif "show_rsvp_neighbors" in request.POST:
                button_name = "show_rsvp_neighbors"
                command = env(str('SHOW_RSVP_NEIGHBORS'))
            
            elif "show_redundancy_summary" in request.POST:
                button_name = "show_redundancy_summary"
                command = env(str('SHOW_REDUNDANCY_SUMMARY'))
            
            elif "show_ospf_neighbor" in request.POST:
                button_name = "show_ospf_neighbor"
                command = env(str('SHOW_OSPF_NEIGHBOR'))
            
            elif "show_ospf_vrf_interface_brief" in request.POST:
                button_name = "show_ospf_vrf_interface_brief"
                command = env(str('SHOW_OSPF_VRF_INTERFACE_BRIEF'))
                
            elif "show_ospf_vrf_neighbor" in request.POST:
                button_name = "show_ospf_vrf_neighbor"
                command = env(str('SHOW_OSPF_VRF_NEIGHBOR'))
            
            
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