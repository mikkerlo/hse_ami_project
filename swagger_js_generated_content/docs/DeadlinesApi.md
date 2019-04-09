# Ami.DeadlinesApi

All URIs are relative to *https://bestdomainever.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**studentStudentIdDeadlinesGet**](DeadlinesApi.md#studentStudentIdDeadlinesGet) | **GET** /student/{student_id}/deadlines | 


<a name="studentStudentIdDeadlinesGet"></a>
# **studentStudentIdDeadlinesGet**
> [HomeTask] studentStudentIdDeadlinesGet(studentId)



### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.DeadlinesApi();

var studentId = 789; // Number | ID of student to return


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.studentStudentIdDeadlinesGet(studentId, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **studentId** | **Number**| ID of student to return | 

### Return type

[**[HomeTask]**](HomeTask.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

