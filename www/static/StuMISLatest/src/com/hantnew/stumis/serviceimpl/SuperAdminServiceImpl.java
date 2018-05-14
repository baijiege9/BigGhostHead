package com.hantnew.stumis.serviceimpl;

import java.util.List;

import com.hantnew.stumis.dao.SuperAdminDao;
import com.hantnew.stumis.daoimpl.SuperAdminDaoImpl;
import com.hantnew.stumis.domain.SuperAdmin;
import com.hantnew.stumis.service.SuperAdminService;

public class SuperAdminServiceImpl implements SuperAdminService {
	
	SuperAdminDao dao = new SuperAdminDaoImpl();
	/* (non-Javadoc)
	 * @see com.hantnew.stumis.serviceimpl.SuperAdminService#add(com.hantnew.stumis.domain.SuperAdmin)
	 */
	@Override
	public boolean add(SuperAdmin superAdmin){
		return dao.add(superAdmin);
	}
    /* (non-Javadoc)
	 * @see com.hantnew.stumis.serviceimpl.SuperAdminService#getSuperAdmins()
	 */
	@Override
	public List<SuperAdmin> getSuperAdmins(){
		return dao.getSuperAdmins();
	}
}
