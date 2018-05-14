<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Insert title here</title>
</head>
<body>

<form action="${pageContext.request.contextPath}/DoSuperAdminCreate">

<table>
<tr>
<td>用户名：</td>
<td><input type="text" name="userNameInput"  value="${myData.getUserName()}" /></td>${myData.getError().username }
</tr>
<tr>
<td>密码：</td>
<td><input type="password" name="passwordInput"  value="${myData.getPassword()}" /></td>${myData.getError().password}
</tr>
<tr>
<td>确认密码：</td>
<td><input type="password" name="repeatPasswordInput"  value="${myData.getRepeatePassword()}"/></td>${myData.getError().repeatepassword}
</tr>
<tr>
<td></td>
<td><input type="submit"  value="创建超级管理员"/></td>
</tr>
</table>

</f.orm>

</body>
</html>