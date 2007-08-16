from django.shortcuts import render_to_response

def simple_tag(request):
	return render_to_response('simple_tag.html')