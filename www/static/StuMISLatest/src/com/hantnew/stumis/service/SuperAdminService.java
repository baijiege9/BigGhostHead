package com.hantnew.stumis.service;

import java.util.List;

import com.hantnew.stumis.domain.SuperAdmin;

public interface SuperAdminService {

	/**
	 * ��ӳ�������Ա
	 * @param SuperAdmin
	 * @return boolean
	 */
	boolean add(SuperAdmin superAdmin);

	/**
	 * ��ѯ��������Ա
	 * @return List<SuperAdmin>
	 */
	List<SuperAdmin> getSuperAdmins();

}