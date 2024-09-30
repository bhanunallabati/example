---
- name: Install and configure Domain Controller
  hosts: windows
  gather_facts: no
  tasks:
    
    - name: Install the Active Directory Domain Services (AD DS) role
      win_feature:
        name: AD-Domain-Services
        include_management_tools: yes
    
    - name: Install the DNS Server role (if required)
      win_feature:
        name: DNS
        include_management_tools: yes
    
    - name: Promote the server to a Domain Controller
      win_domain:
        dns_domain_name: "yourdomain.com"  # Change to your domain name
        safe_mode_password: "{{ 'P@ssw0rd' | password_hash('sha512') }}"  # Change password and use a vault-encrypted value for better security
        domain_netbios_name: "YOURDOMAIN"  # Optional: Change NetBIOS name if required
        domain_admin_user: "Administrator"
        domain_admin_password: "{{ win_password }}"  # Use a variable for the admin password
        forest_level: "2016"
        domain_level: "2016"
        install_dns: yes
        state: "domain_controller"
        restart: yes

    - name: Reboot server if required
      win_reboot:
        reboot_timeout: 3600
