# Ami.GroupApi

All URIs are relative to *https://bestdomainever.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**groupPost**](GroupApi.md#groupPost) | **POST** /group | 
[**studentStudentIdGroupsGet**](GroupApi.md#studentStudentIdGroupsGet) | **GET** /student/{student_id}/groups | 


<a name="groupPost"></a>
# **groupPost**
> groupPost(data)



### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.GroupApi();

var data = new Ami.Group(); // Group | Data of group to create


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.groupPost(data, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data** | [**Group**](Group.md)| Data of group to create | 

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="studentStudentIdGroupsGet"></a>
# **studentStudentIdGroupsGet**
> [Group] studentStudentIdGroupsGet(studentId)



### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.GroupApi();

var studentId = 789; // Number | ID of student to return


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.studentStudentIdGroupsGet(studentId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **studentId** | **Number**| ID of student to return | 

### Return type

[**[Group]**](Group.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

