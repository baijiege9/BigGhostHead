package com.hantnew.stumis.daoimpl;

import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

import com.hantnew.stumis.dao.SuperAdminDao;
import com.hantnew.stumis.domain.SuperAdmin;
import com.hantnew.stumis.tools.SqlHelper;

public class SuperAdminDaoImpl implements SuperAdminDao {
    SqlHelper helper = new SqlHelper();
	//超级管理员帐户的创建（添加）。
	/* (non-Javadoc)
	 * @see com.hantnew.stumis.daoimpl.SuperAdminDao#add(com.hantnew.stumis.domain.SuperAdmin)
	 */
	@Override
	public boolean add(SuperAdmin admin){
		boolean result=false;
		try{
			String sql ="insert into SuperAdmins(userName,[password]) values(?,?)";
			String[] paras={admin.getUserName(),admin.getPassword()};
		   if(helper.updateExecute(sql, paras)){
			   result=true;
		   }
		}catch(Exception e){
			e.printStackTrace();
		}
		return result;
	}
	
	//超级管理员帐户查询
	
	/* (non-Javadoc)
	 * @see com.hantnew.stumis.daoimpl.SuperAdminDao#getSuperAdmins()
	 */
	@Override
	public List<SuperAdmin> getSuperAdmins(){
		try{
			String sql="select * from SuperAdmins";
			ResultSet rs=helper.queryExecute(sql, null);
			List<SuperAdmin> superAdmins = new ArrayList<SuperAdmin>();
			while(rs.next()){
				SuperAdmin superAdmin = new SuperAdmin();
				superAdmin.setUserName(rs.getString(1));
				superAdmin.setPassword(rs.getString(2));
				superAdmins.add(superAdmin);
			}
			return superAdmins;
		}catch(Exception e){
			e.printStackTrace();
			return null;
		}
	}
}
