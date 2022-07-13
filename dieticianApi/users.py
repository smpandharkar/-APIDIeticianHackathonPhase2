from flask import request
from flask_restx import Resource,Namespace, fields
import controller as dynamodb
import commonFunc as PRE_REQUISITE
import key_constants as PREFIX

api = Namespace("Users API", description="All the API's for User Data")

address_field = {}
address_field['Address1'] = fields.String(readOnly=True, description='Address line 1')
address_field['Address2'] = fields.String(readOnly=True, description='Address line 2')
address_field['City'] = fields.String(readOnly=True, description='City of the user')
address_field['State'] = fields.String(readOnly=True, description='State of the user')
address_field['Country'] = fields.String(readOnly=True, description='Country of the user')


user_put = api.model('UsersApi', {
    'FirstName': fields.String(required=True, description='First Name of the user'),
    'LastName': fields.String(required=True, description='Last Name of the user'),
    'Address': fields.Nested(api.model('address_field', address_field)),
    'Contact': fields.String(required=True, description='Contact number of the user'),
    'Email': fields.String(required=True, description='Email Address of the user'),
    'FoodCategory': fields.String(required=True, description='FoodCategory of the user'),
    'Allergy': fields.String(required=True, description="User's Allergy"),
})




class UsersApi(Resource):
    def get(self, FirstName=None, Email=None, Contact=None, UserType=None, DieticianId=None):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_all('InfoType', 'User', projectionexp)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Items' in response:
                return {'Items': response['Items']}
            return {'Message': 'Items not found!'}
        return {
            'Message': 'Some error occurred',
            'response': response
        }

    def post(self):
        # data['InfoType'],data['UserId'],data['FirstName'],data['LastName'],data['Address'],data['Contact']
        # data['Email'],data['Allergy'],data['FoodCategory'],data['DieticianId'],data['LoginUsername'],data['Password']
        data = request.get_json()
        status_flag  = PRE_REQUISITE.validate_request_body(data,'user')  # Coding not completed
        print ('Status :',status_flag)
        if len(status_flag)==0:
            auto_user_id = PRE_REQUISITE.generate_user_id(data['UserType'])
            if data['UserType']=='Dietician': data['DieticianId']=auto_user_id
            if bool(auto_user_id):
                response = dynamodb.write_user(auto_user_id, data)
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return {
                        'UserId': auto_user_id,
                        'Message': 'User successful created.'
                    }
                return {
                    'Message': 'error occurred',
                    'response': response
                }
        return {
                'Message': 'Missing Items OR Invalid Entry.Check on ' + str(status_flag)
              }

    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    @api.expect(user_put)
    @api.doc(params={
        'DieticianId': 'Id of the Dietician',
        'UserId': 'Type of the user'
    })
    def put(self,DieticianId,UserId):
        data = request.get_json()
        response = dynamodb.update_user(DieticianId, UserId, data)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                "UserId" 	: UserId,
                'FirstName': data['FirstName'],
                'Message': 'User updated successful',
            }
        return {
            'Message': 'error occurred',
            'response': response
        }

    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    @api.doc(params={
        'DieticianId': 'Id of the Dietician',
        'UserId': 'Type of the user'
    })
    def delete(self,DieticianId,UserId):
        response = dynamodb.delete_user(DieticianId, UserId)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {
                'DieticianId': dietician_id,
                'UserId': user_id,
                'Message': 'Successfully Deleted.'
            }
        return {
            'Message': 'error occurred',
            'response': response
        }


class UserFirstNameAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'FirstName': 'First Name of the user'})
    def get(self,FirstName):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('FirstName', FirstName, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserEmailAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'Email': 'Email of the user'})
    def get(self,Email):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('Email', Email, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserContactAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'Contact': 'Contact of the user'})
    def get(self,Contact):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('Contact', Contact, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserTypeAPI(Resource):
    @api.doc(responses={ 200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'UserType': 'Type of the user'})
    def get(self,UserType):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_attr_that_contains_value('UserType', UserType, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

class UserDieticianIdAPI(Resource):
    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    @api.doc(params={'DieticianId': 'Id of the Dietician'})
    def get(self, DieticianId):
        projectionexp = 'UserId, FirstName, LastName, Address, Contact, Email, FoodCategory, Allergy'
        response = dynamodb.read_all('DieticianId', DieticianId, projectionexp)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            if ('Items' in response):
                return response
            return {'msg': 'Item not found!'}
        return {
            'msg': 'error occurred',
            'response': response
        }

#endpoints for User
api.add_resource(UserFirstNameAPI, '/FirstName=<FirstName>', methods=['GET'])
api.add_resource(UserEmailAPI, '/Email=<Email>', methods=['GET'])
api.add_resource(UserContactAPI, '/Contact=<Contact>', methods=['GET'])
api.add_resource(UserTypeAPI, '/UserType=<UserType>', methods=['GET'])
api.add_resource(UserDieticianIdAPI, '/DieticianId=<DieticianId>', methods=['GET'])
api.add_resource(UsersApi, '/DieticianId=<DieticianId>&UserId=<UserId>', methods=['PUT','DELETE'])
api.add_resource(UsersApi, '/', methods=['POST'])