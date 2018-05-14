package com.hantnew.stumis.viewmodel;

import java.util.HashMap;
import java.util.Map;

import com.hantnew.stumis.service.SuperAdminService;
import com.hantnew.stumis.serviceimpl.SuperAdminServiceImpl;

public class SuperAdminViewModel {
private String userName;
private String password;
private String repeatePassword;
private Map<String,String > error=new HashMap<String,String>();

SuperAdminService service = new SuperAdminServiceImpl();
public Map<String, String> getError() {
	return error;
}
public String getUserName() {
	return userName;
}
public void setUserName(String userName) {
	this.userName = userName;
}
public String getPassword() {
	return password;
}
public void setPassword(String password) {
	this.password = password;
}
public String getRepeatePassword() {
	return repeatePassword;
}
public void setRepeatePassword(String repeatePassword) {
	this.repeatePassword = repeatePassword;
}

public boolean validate(){
	
	if (userName==null || userName.trim().equals("")){
		error.put("username", "�û�������Ϊ�գ�");
	   return false;
	}else if( !service.getSuperAdmins().isEmpty()){
		error.put("username", "��������Ա�ʻ��Ѿ����ڣ������ظ�������");
		return false;
	}else if(password==null ||password.trim().equals("")){
		error.put("password","���벻��Ϊ�գ�");
		return false;
	}else if(! repeatePassword.equals(password)){
		error.put("repeatepassword","������������벻һ�£�");
		return false;
	}else{
		return true;
	}
	
}
}
