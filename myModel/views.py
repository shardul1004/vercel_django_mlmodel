from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.renderers import JSONRenderer  # Import the JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import serializers
from keras.models import load_model

class InputDataSerializer(serializers.Serializer):
    Type = serializers.CharField()
    Days_for_shipment_scheduled = serializers.IntegerField()
    Late_delivery_risk = serializers.IntegerField()
    Category_Name = serializers.CharField()
    Customer_City = serializers.CharField()
    Customer_Segment = serializers.CharField()
    Order_City = serializers.CharField()
    Shipping_Mode = serializers.CharField()
    Product_Name = serializers.CharField()


@api_view(['GET','POST'])  # Adjust the HTTP method as needed
def predict(request):
    if request.method == 'GET':
        return Response({"error": "Please use POST Method to make a prediction"})
    NNmodel = load_model('myModel\supply_chain.h5')
    if request.method == 'POST':
        try:
            # Parse the form data using the InputDataSerializer
            serializer = InputDataSerializer(data=request.data)
            if serializer.is_valid():
                input_data = serializer.validated_data
                # Create a DataFrame from the input data
                # input_df = pd.DataFrame([input_data])
                # Assuming 'random_forest' is trained on the same features in X
                predictions = NNmodel.predict(input_data)
                # Set the renderer
                return Response({'predictions': predictions.tolist()})
            else:
                # Set the renderer
                return Response({'error':serializer.errors})
        except Exception as e:
            # Set the renderer
            return Response({'error': str(e)})

    # Set the renderer
    return Response({'error': 'Invalid request method'})
