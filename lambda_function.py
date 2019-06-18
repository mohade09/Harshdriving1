from __future__ import print_function
  
import json
import boto3
  
print('Loading function')
  
def lambda_handler(event, context):
  
    # Parse the JSON message 
    eventText = json.dumps(event)
    
    eventtext1 = json.loads(eventText)
    
   # parsed JSON messages from the incoming stream, currentspeed is the speed at time t, and currentspeed_t1,currentspeed_t2
   # are the speed at t-1 ,t-2 interval. Two previous reading from the vechicle.
   # simulator is currently passing last two reading along with current speed
   
   
    cspeed = eventtext1["speed"]
    cspeed1 = eventtext1["speed1"]
    cspeed2 = eventtext1["speed2"]
    
    # Print the parsed JSON message to the console; you can view this text in the Monitoring tab in the Lambda console or in the CloudWatch Logs console
    print('Received event: ', eventText)
    print('Received speed event: ', cspeed)
    print('Received speed event1: ', cspeed1)
    print('Received speed event2: ', cspeed2)
    
    tmp1 = cspeed1-cspeed 
    print('Received speed tmp1: ', tmp1)
    tmp2 = (cspeed2-cspeed1)
    print('Received speed tmp2: ', tmp2)
    
    # condition the current speed is greater than 20PMPh
    # and last two concucative speed decreases by at least 9 MPH per second for three consecutive calculations
    
    # speed@t1 -speed@t  >= 9 & speed@t2 - speed@t1 >= 9 -> condition for harsh breaking
    
    if ( cspeed > 20 ):
     if ( tmp1 >= 9):  # tmp1 = speed@t1 -speed@t
       if ( tmp2 >= 9):print ("harsh breaking scenario") # tmp2 = speed@t2 -speed@t1
       else: print ("Not Harsh breaking")
     else: print ("Not Harsh breaking")
    else: print ("speed is not enough for Harshbreaking condition")
    
    
    
    # Create an SNS client
    sns = boto3.client('sns')
  
    # Publish a message to the specified topic
    response = sns.publish (
      TopicArn = 'arn:aws:sns:eu-west-1:345103262615:mylambdafunctionrole',
      Message = eventText
    )
  
    print(response)