import os
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai


def generate_prompt(subject, question, user_type="learner"):
  """Generates a prompt for the request."""
  if user_type == "teacher":
    return f"Create a lesson plan for a 2nd grade on {subject} relating to {question} with relevant examples. Provide learning objectives, activities, assessments, and materials. provide a daily, weekly and monthly plan for detail student centered approach"
  else:
    return f"Generate a lecture on {subject} relating to {question} with relevant examples. Provide illustration diagrams if applicable. Suggest major steps to experiment if applicable."


class TutorView(APIView):
  """API endpoint to generate a tutoring lesson."""
  throttle_classes = [AnonRateThrottle, UserRateThrottle]  # Apply rate limiting

  def post(self, request):
    """Handles POST requests to generate a tutoring lesson."""
    subject = request.data.get('subject')
    question = request.data.get('question')
    user_type = request.data.get('user_type', "learner")  # Default to learner

    if not subject:
      return Response({'error': 'Subject is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not question:
      return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)

    prompt = generate_prompt(subject, question, user_type)

    try:
      response = model.generate_content(prompt)
      lesson_content = response.text  # Extract the text content from the response

      return Response({'lesson': lesson_content}, status=status.HTTP_200_OK)
    except Exception as e:
      # Handle potential errors from the LLM model
      return Response({'error': f"Error generating lesson: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Configure the API key (from environment variable)
genai.configure(api_key=os.getenv('GOOGLE_GEMINI_KEY'))

# Select the model
model = genai.GenerativeModel('gemini-1.5-flash')
