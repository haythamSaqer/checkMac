from django.shortcuts import render, redirect, HttpResponse
import requests

from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Mac, Erorr
from .serializers import MacSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class MacListView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Mac.objects.all()
    serializer_class = MacSerializer
    pagination_class = StandardResultsSetPagination




class MacsList(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


    """
    List all Macs, or create a new mac.
    """
    def get(self, request, format=None):
        mac = Mac.objects.all()
        serializer = MacSerializer(mac, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MacSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def post_mac(request):
    list1 = []
    # if Mac.objects.all() is not None:
    #     return redirect('test')
    # else:
    with open('task/mac-vendor2.txt') as list:
        for i in list:
            mac = i.strip().split("\t")[0]
            vendor = i.strip().split("\t")[1]
            dict = {}
            list1.append(dict)
            dict['mac'] = mac
            dict['vendor'] = vendor
        for i in list1:
            requests.post('http://127.0.0.1:8000/customerList/', i)


        # pointer = 0
        # new_list = []
        # for i in list1:
        #     if pointer <= 10:
        #         new_list.append(i)
        #         pointer += 1
        #     else:
        #         pointer = 0
        #         r = requests.post('http://127.0.0.1:8000/customerList/', data={'data': new_list})
        #         new_list = []
    return redirect('test')


"""

class Mac(models.Model):
    CHOICES = [
        ('Basic', 'Basic'),
        ('Business', 'Business'),
        ('Agency', 'Agency'),

    ]
    mac = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200)
    requestCounter = models.IntegerField(null=True)
    subscriptionPlan = models.CharField(choices=CHOICES, max_length=20, null=True)

"""

@api_view
def up_grade(request):
    return Response({'upgrade now': 'upgrade'})



class CheckMac(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MacSerializer

    def get_queryset(self):
        if self.request.user.subscriptionPlan == 'Basic':
            if self.request.user.requestCounter <= 50:
                self.request.user.requestCounter += 1
                print(self.request.user.requestCounter)
                self.request.user.save()
                queryset = Mac.objects.all()
                mac = self.request.query_params.get('mac', None)
                if mac is not None:
                    queryset = queryset.filter(mac__icontains=mac)

                return queryset
            else:
                upgrade = Erorr.objects.values('erorr',)
                queryset = upgrade
                return queryset
        elif self.request.user.subscriptionPlan == 'Business':
            if self.request.user.requestCounter <= 150:
                self.request.user.requestCounter += 1
                queryset = Mac.objects.all()
                mac = self.request.query_params.get('mac', None)
                if mac is not None:
                    queryset = queryset.filter(mac__icontains=mac)
                return queryset
            else:
                return redirect('upgrade')
        elif self.request.user.subscriptionPlan == 'Agency':
            if self.request.user.requestCounter <= 500:
                ++self.request.user.requestCounter
        else:
            return HttpResponse('you need to choice a new plan ')

        # if self.request.user.subscriptionPlan == 'Basic':
        #     if self.request.user.requestCounter <= 50:
        #         self.request.user.requestCounter += 1
        #         print(self.request.user.requestCounter)
        #         self.request.user.save()
        #         # self.get()
        #     else:
        #         return HttpResponse('you need to upgrade')
        #
        # elif self.request.user.subscriptionPlan == 'Business':
        #     if self.request.user.requestCounter <= 150:
        #         self.request.user.requestCounter += 1
        #         # self.get()
        #     else:
        #         return HttpResponse('you need to upgrade')
        #
        # elif self.request.user.subscriptionPlan == 'Agency':
        #     if self.request.user.requestCounter <= 500:
        #         ++self.request.user.requestCounter
        #         # self.get()
        # else:
        #     return HttpResponse('you need to choice a new plan ')
        # queryset = Mac.objects.all()
        # mac = self.request.query_params.get('mac', None)
        # if mac is not None:
        #     queryset = queryset.filter(mac__icontains=mac)
        # return queryset



    # serializer_class = MacSerializer
    #
    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = Mac.objects.all()
    #     username = self.request.query_params.get('mac')
    #     if username is not None:
    #         queryset = queryset.filter(mac__icontains=username)
    #     return queryset


# class (generics.ListAPIView):
#     serializer_class = MacSerializer
#
#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = Mac.objects.all()
#         mac = self.request.query_params.get('mac', None)
#         if mac is not None:
#             queryset = queryset.filter(mac__icontains=mac)
#         return queryset

class MacCheckList(generics.ListAPIView):

    # def get_queryset(self):
    #     data = self.queryset.values('mac')
    #     print(data)
    #
    #     mac = self.queryset.all()
    #     serializer = MacSerializer(mac, many=True)
    #
    #     return Response(serializer.data)


    queryset = Mac.objects.all()
    serializer_class = MacSerializer
    filter_backends = []
    search_fields = ['mac']

