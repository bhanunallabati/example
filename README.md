To use the `Install-ADDSDomainController` PowerShell command in an Ansible playbook, you can run it via the `win_shell` module since there is no direct Ansible module for this PowerShell command. Below is an Ansible playbook that promotes an existing Windows Server in an Active Directory domain to a Domain Controller using `Install-ADDSDomainController`.

### **Ansible Playbook Using `Install-ADDSDomainController`**

```yaml
---
- name: Promote Windows Server to Domain Controller
  hosts: windows
  gather_facts: no
  tasks:
    
    - name: Install the Active Directory Domain Services (AD DS) role
      win_feature:
        name: AD-Domain-Services
        include_management_tools: yes

    - name: Install DNS Server role (if required)
      win_feature:
        name: DNS
        include_management_tools: yes

    - name: Promote the server to a Domain Controller
      win_shell: |
        Install-ADDSDomainController `
          -DomainName "yourdomain.com" `
          -Credential (New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList '{{ domain_admin_user }}', (ConvertTo-SecureString '{{ domain_admin_password }}' -AsPlainText -Force)) `
          -SafeModeAdministratorPassword (ConvertTo-SecureString '{{ safe_mode_password }}' -AsPlainText -Force) `
          -InstallDNS:$true `
          -Force:$true `
          -NoRebootOnCompletion:$false
      args:
        executable: powershell
      vars:
        domain_admin_user: Administrator
        domain_admin_password: "{{ win_password }}"  # Replace with secure password or use vault
        safe_mode_password: "P@ssw0rd"  # Replace with secure password or use vault
    
    - name: Reboot the server if required
      win_reboot:
        reboot_timeout: 3600
```

### **Explanation**:

- **Install-ADDSDomainController**: The PowerShell command used to promote the server to a Domain Controller.
- **win_shell**: Runs the PowerShell command within the Ansible playbook.
- **win_feature**: Installs necessary features (AD DS, DNS).
- **win_reboot**: Restarts the server after the promotion to Domain Controller.

### **Variables**:

- `domain_admin_user`: The domain administrator user.
- `domain_admin_password`: The domain administrator password (use Ansible Vault to encrypt this securely).
- `safe_mode_password`: The Safe Mode Administrator password (use Ansible Vault to encrypt this securely).

### **Inventory File Example (hosts)**:

```ini
[windows]
winserver1 ansible_host=192.168.1.10 ansible_user=Administrator ansible_password=YourPassword ansible_port=5986 ansible_connection=winrm ansible_winrm_server_cert_validation=ignore
```

### **Execution**:

- Save the playbook to a file, e.g., `promote_dc.yml`.
- Run the playbook with the command:

```bash
ansible-playbook -i hosts promote_dc.yml
```

### **Additional Notes**:

- Make sure that the target server is already part of an existing domain.
- The password for `domain_admin_password` and `safe_mode_password` should be encrypted using Ansible Vault for security.
- If there are any issues related to the execution of the `win_shell` command, ensure that PowerShell is properly configured on the target Windows machine, and WinRM is properly set up for remote execution.

This playbook will promote the server to a domain controller in the existing Active Directory domain.
