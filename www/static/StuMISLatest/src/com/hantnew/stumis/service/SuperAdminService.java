package com.hantnew.stumis.service;

import java.util.List;

import com.hantnew.stumis.domain.SuperAdmin;

public interface SuperAdminService {

	/**
	 * 添加超级管理员
	 * @param SuperAdmin
	 * @return boolean
	 */
	boolean add(SuperAdmin superAdmin);

	/**
	 * 查询超级管理员
	 * @return List<SuperAdmin>
	 */
	List<SuperAdmin> getSuperAdmins();

}