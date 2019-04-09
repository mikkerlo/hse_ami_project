# Ami.StudentApi

All URIs are relative to *https://bestdomainever.com/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**addPet**](StudentApi.md#addPet) | **GET** /student | Get students data
[**studentIdGet**](StudentApi.md#studentIdGet) | **GET** /student/{id} | 
[**studentIdPatch**](StudentApi.md#studentIdPatch) | **PATCH** /student/{id} | Update some info about student
[**studentPost**](StudentApi.md#studentPost) | **POST** /student | Create user 
[**studentStudentIdDeadlinesGet**](StudentApi.md#studentStudentIdDeadlinesGet) | **GET** /student/{student_id}/deadlines | 
[**studentStudentIdGroupsGet**](StudentApi.md#studentStudentIdGroupsGet) | **GET** /student/{student_id}/groups | 


<a name="addPet"></a>
# **addPet**
> [Student] addPet(offset, count)

Get students data

Returns &#x60;count&#x60; students from offset &#x60;offset&#x60;. 

### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.StudentApi();

var offset = 56; // Number | Offset to start with 

var count = 56; // Number | Number of returned records 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.addPet(offset, count, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **offset** | **Number**| Offset to start with  | 
 **count** | **Number**| Number of returned records  | 

### Return type

[**[Student]**](Student.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="studentIdGet"></a>
# **studentIdGet**
> Student studentIdGet(id)



### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.StudentApi();

var id = 789; // Number | ID of student to return


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.studentIdGet(id, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| ID of student to return | 

### Return type

[**Student**](Student.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="studentIdPatch"></a>
# **studentIdPatch**
> studentIdPatch(id, data)

Update some info about student

Gets dictionary with student&#39;s description, then updates these fields in  database. 

### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.StudentApi();

var id = 789; // Number | ID of student to return

var data = new Ami.StudentPost(); // StudentPost | New data to store


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.studentIdPatch(id, data, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| ID of student to return | 
 **data** | [**StudentPost**](StudentPost.md)| New data to store | 

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="studentPost"></a>
# **studentPost**
> studentPost(data)

Create user 

Creates new user in system 

### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.StudentApi();

var data = new Ami.StudentPost(); // StudentPost | New student data.  


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.studentPost(data, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data** | [**StudentPost**](StudentPost.md)| New student data.   | 

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="studentStudentIdDeadlinesGet"></a>
# **studentStudentIdDeadlinesGet**
> [HomeTask] studentStudentIdDeadlinesGet(studentId)



### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.StudentApi();

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

<a name="studentStudentIdGroupsGet"></a>
# **studentStudentIdGroupsGet**
> [Group] studentStudentIdGroupsGet(studentId)



### Example
```javascript
var Ami = require('ami');

var apiInstance = new Ami.StudentApi();

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

