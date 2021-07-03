exist_stack=$(aws cloudformation describe-stacks --stack-name CfnEc2 --query "Stacks[0].StackId"  --output text)

echo $exist_stack
# check if it is first time to create the stack 
if [ -z "$exist_stack" ]
then 
	# if existing stack does not exist 
	echo "create new stack"
	# create new elastic ip for the stack
	aws cloudformation create-stack --template-body file://pre_cfn_deploy.yaml --stack-name PreCfnEc2
    echo "check "

	ip=$(aws ssm get-parameters --names elastic-ip --query "Parameters[*].{Value:Value}" --output text)

	while ! [ "${ip}" ]; do
	echo "sleep for 10 secs"
	sleep 10 ;
	ip=$(aws ssm get-parameters --names elastic-ip --query "Parameters[*].{Value:Value}" --output text)
	done

	# create the EC2 instance and associate the elastic ip to the instance
	aws cloudformation create-stack --template-body file://cfn_main1.yaml --stack-name CfnEc2 --parameters file://parameters.json

# check if the stack exists  
else 
	echo "stack exists, delete existing stack"

	# delete stack 
	aws cloudformation delete-stack --stack-name CfnEc2 

	exist_stack=$(aws cloudformation describe-stacks --stack-name CfnEc2 --query "Stacks[0].StackId"  --output text)

	echo "wait until deletion is successful"
	while  [ "${exist_stack}" ]; do
	echo "sleep for 10 secs"

	sleep 10 ;
	exist_stack=$(aws cloudformation describe-stacks --stack-name CfnEc2 --query "Stacks[0].StackId"  --output text)
	done 

	# wait until deletion is successful, create the stack 
	echo "create stack"
	aws cloudformation create-stack --template-body file://cfn_main1.yaml --stack-name CfnEc2 --parameters file://parameters.json


fi