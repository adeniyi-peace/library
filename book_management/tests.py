from django.test import TestCase

#Create your tests here.


# import requests
# import json



# def jprint(obj):
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

# def test(request):
#     start = input("enter ISBN:")
#     response = requests.get(f"https://openlibrary.org/isbn/{start}.json")
#     work = response.json()
#     jprint(work)
#     try:
#         book = Book(title=work.get("title"), ISBN=start,description=work.get("description"),
#                     page_count=work.get("number_of_pages"))
#         book.save()
#     except Exception as error:
#         print(error)
#         print("An error occured")

    
#     return render(request, "book_management/index.html")