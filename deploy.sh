
instance_id=`aws ec2 describe-instances \
    --filters "Name=tag-value,Values=ec2app" --query 'Reservations[*].Instances[*].{Instance:InstanceId}' --output text`

echo $instance_id
if [ -z "$instance_id" ]
then 

	echo "instance does not exist"
else 
	echo "instance exists, terminate $instance_id"
	aws ec2 terminate-instances --instance-ids $instance_id

fi

instance_id=$(aws ec2 run-instances --image-id ami-0186908e2fdeea8f3 --instance-type t2.micro --region ap-southeast-2   \
--key-name ec2_id_rsa  --user-data file://ud.txt --count 1 --tag-specifications 'ResourceType=instance,Tags=[{Key=task,Value=ec2app1}]' 'ResourceType=volume,Tags=[{Key=task,Value=ec2app1}]'  --output text  --query 'Instances[*].InstanceId') 


ip=$(aws ssm get-parameters --names public-ip --query "Parameters[*].{Value:Value}" --output text)


if [ -z "$ip" ]
then 
	ip=$( aws ec2 allocate-address --tag-specifications 'ResourceType=elastic-ip ,Tags=[{Key=task,Value=ec2app}]' --output text  --query 'PublicIp' )
	
	aws ssm put-parameter --name "public-ip" --value $ip= --type String --tags "Key=task,Value=ec2app"

aws ec2 associate-address --instance-id $instance_id --public-ip $ip 
