package com.hantnew.stumis.dao;

import java.util.List;

import com.hantnew.stumis.domain.SuperAdmin;

public interface SuperAdminDao {

	//��������Ա�ʻ��Ĵ�������ӣ���
	boolean add(SuperAdmin admin);

	List<SuperAdmin> getSuperAdmins();

}