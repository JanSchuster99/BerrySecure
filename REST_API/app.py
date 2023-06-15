from flask import Flask, request, jsonify, make_response, render_template
from flask_restful import Resource, Api
from RNGRaspPi import *
from init import init
from shutdown import die
from RNGRaspPiTests import onlineTest, totTest

TRNG_RUNNING = False
app = Flask(__name__)
api = Api(app)
api.prefix = '/trng'


class GetRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        if(not TRNG_RUNNING):
            # Status code 432 if system is not ready to generate random numbers
            return make_response(jsonify({'description': 'system not ready; try init'}), 432)
        # Get the quantity of streams and number of bits in each stream
        quantity = request.args.get('quantity', default=1)
        numBits = request.args.get('numBits', default=1)
        # Set parameters to integers if both inputs are numeric
        if quantity.isnumeric():
            quantity = int(quantity)
        if numBits.isnumeric():
            numBits = int(numBits)
        # Status code 400 if input is not numeric
        if not type(numBits) == int or not type(quantity) == int:
            response = make_response(jsonify({'description': 'not a numeric input, please enter a valid input'}), 400)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        # Status code 400 if input is not greater than 0 or greater than 2^26 
        if numBits < 1 or quantity < 1:
            response = make_response(jsonify({'description': 'input must be greater than 0, please enter a valid input'}), 400)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response 
        if numBits*quantity > 2**26:
            response = make_response(jsonify({'description': 'no more than 67108864 random bits can be generated at once, please choose number of Bits and quantity accordingly'}), 400)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response 
        # Generate a random number and test if TRNG is still working
        testNumber = generateRandomNumber(2*10**5,1)
        # Status code 445 if microphone is not connected
        if testNumber == "":
            response = make_response(jsonify({'description': 'microphone not connected'}), 445)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        if(totTest(testNumber) and onlineTest(testNumber)):
            # Generate the random number with desired parameters
            temp = generateRandomNumber(numBits, quantity)
            # GenerateRandomNumber returns empty string if microphone is not connected
            if temp == "":
                response = make_response(jsonify({'description': 'microphone not connected'}), 445)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            # Bit streams get encoded in hex
            result = encode_in_hex(numBits, temp)
            result_str = ",".join(str(i) for i in result)

            data = {
                'description': 'successful operation; HEX-encoded bit arrays (with leading zeros if required)',
                'randomBits': result
            }
            # Return the collected data
            if(len(result) > 0):
                response = make_response(jsonify(data), 200)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            # Status code 445 if microphone is not connected
            else:
                response = make_response(jsonify({'description': 'microphone not connected'}), 445)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
        # Status code 543 if online test failed
        else:
                response = make_response(jsonify({'message': 'online test failed'}), 543)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
             

# This endpoint initializes the TRNG and ensures that the endpoint GetRandomNums works.
class InitRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        # Status code 409 if system is already running 
        if(TRNG_RUNNING):
            response = make_response(jsonify({'description': 'system already running'}), 409)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            # If TRNG isnt running init system or throw erros if it takes too long, startup tests failed or the mic is not connected
            initialized = init()
            # Status code 200 if system is running successfully
            if(initialized ==200):
                TRNG_RUNNING = True
                response = make_response(jsonify({'description': 'successful operation; random number generator is ready and random numbers can be requested'}), 200)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            # Status code 555 if TRNG is unable to initialize within 60s
            elif(initialized ==555):
                response = make_response(jsonify({'description': 'unable to initialize the random number generator within a timeout of 60 seconds'}), 555)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            # Status code 543 if startup test failed
            elif(initialized ==543):
                response = make_response(jsonify({'description': 'startup test failed'}), 543)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            # Status code 445 if microphone is not connected
            elif(initialized ==409):
                response = make_response(jsonify({'description': 'microphone not connected'}), 445)
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
          

class ShutdownRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        if(TRNG_RUNNING):
            # Shuts down the radio
            die()
            TRNG_RUNNING = False
            response = make_response(jsonify({'description': 'successful operation; random number generator has been set to \"standby mode\"'}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        # Status code 409 if system is already shut down
        else:
            response = make_response(jsonify({'description': 'system already shut down'}), 409)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        

# This endpoint is the home directory.
class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)
    
api.add_resource(GetRandomNums, '/randomNum/getRandom')
api.add_resource(InitRandomNums, '/randomNum/init')
api.add_resource(ShutdownRandomNums, '/randomNum/shutdown')
api.add_resource(Home, '/')

if __name__ == '__main__':
     app.run(ssl_context=('/home/berrysecure/REST_API/cert.pem', '/home/berrysecure/REST_API/key.pem'), host='172.16.78.55', port='8080')