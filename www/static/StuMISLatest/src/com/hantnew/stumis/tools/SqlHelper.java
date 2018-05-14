package com.hantnew.stumis.tools;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class SqlHelper {

	//1��������صı���
	Connection con = null;
	String dbUrl="jdbc:sqlserver://localhost:1433;DatabaseName=StuMIS";
	String user="sa";
	String password="sasa123456";
	String driver="com.microsoft.sqlserver.jdbc.SQLServerDriver";
	ResultSet rs=null;
	PreparedStatement ps =null;
	//2������������ݿ�ķ���������ɾ���ġ���
	//��1����������ɾ���ķ���
	public boolean updateExecute(String sql, String[] paras){
		boolean result= false;
		try{
			//1����������
			Class.forName(driver);
			//2����ȡ���Ӷ���
			con = DriverManager.getConnection(dbUrl, user, password);
			//3������ps
			ps=con.prepareStatement(sql);
			//4���������
			if(paras !=null){
				for(int i=0;i<paras.length;i++){
					ps.setString(i+1, paras[i]);
				}
			}
			//5��ִ�в���
		   if(ps.executeUpdate()==1){
			   result=true;
		   }
		}catch(Exception e){
			e.printStackTrace();
		}finally{
			try{
			if(con !=null){
				con.close();
			}
			if(ps !=null){
				ps.close();
			}
			}catch(Exception e){
				e.printStackTrace();
			}
		}
		return result;
	}
	
	//��2�����ݲ�ѯ����
	public ResultSet queryExecute(String sql, String[] paras){
		try{
			//1����������
			Class.forName(driver);
			//2����ȡ���Ӷ���
			con = DriverManager.getConnection(dbUrl, user, password);
			//3������ps
			ps=con.prepareStatement(sql);
			//4���������
			if(paras !=null){
				for(int i=0;i<paras.length;i++){
					ps.setString(i+1, paras[i]);
				}
			}
			//5��ִ�в���
			 rs= ps.executeQuery();
		}catch(Exception e){
			e.printStackTrace();
		}
		return rs;
	}
	
}
