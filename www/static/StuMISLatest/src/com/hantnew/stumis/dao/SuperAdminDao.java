package com.hantnew.stumis.dao;

import java.util.List;

import com.hantnew.stumis.domain.SuperAdmin;

public interface SuperAdminDao {

	//超级管理员帐户的创建（添加）。
	boolean add(SuperAdmin admin);

	List<SuperAdmin> getSuperAdmins();

}