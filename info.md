sudo certbot certonly --dns-route53 \
  -d "leonardeshun.com" \
  -d "*.leonardeshun.com" \
  --post-hook "systemctl reload nginx" \
  --force-renewal

Using an IAM Role is the most secure method because you won't have any secret keys sitting in text files on your server.1. Create the IAM RoleGo to the IAM Console in AWS.Click Roles > Create role.Select AWS service as the trusted entity and choose EC2.On the permissions page, click Create policy.Switch to the JSON tab and paste the policy from the previous message (make sure to replace YOUR_HOSTED_ZONE_ID with your actual Route 53 zone ID).Finish creating the policy, then go back to your Role creation, refresh the list, and attach that new policy.Name the role something like CertbotRoute53Role and save it.2. Attach the Role to your EC2 InstanceGo to the EC2 Console and select your running instance.Click Actions > Security > Modify IAM role.Select the CertbotRoute53Role you just created and click Update IAM role.3. Run CertbotNow, Certbot will automatically "ask" the EC2 instance metadata for credentials. You don't need to specify any credential files. Run this command:bashsudo certbot certonly --dns-route53 -d "leonardeshun.com" -d "*.leonardeshun.com"
Use code with caution.4. Set Up the Auto-ReloadSince Certbot will now handle the renewal in the background, you just need to make sure your web server (Nginx or Apache) picks up the new files when they change.Run this once to tell Certbot to reload your server after every successful renewal:bashsudo certbot renew --dry-run --post-hook "systemctl reload nginx"
Use code with caution.(Swap nginx for apache2 if you are using Apache).Success! Your wildcard cert is now "set it and forget it." It will renew every 60-90 days and your server will automatically start using the new one.Would you like the command to find your Hosted Zone ID if you don't have it handy?



sudo yum reinstall -y python3-cryptography python3-pyOpenSSL

sudo /usr/bin/python3 -m pip install -U --force-reinstall --ignore-installed urllib3 requests cryptography certbot