package com.hantnew.stumis.tools;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class SqlHelper {

	//1、定义相关的变量
	Connection con = null;
	String dbUrl="jdbc:sqlserver://localhost:1433;DatabaseName=StuMIS";
	String user="sa";
	String password="sasa123456";
	String driver="com.microsoft.sqlserver.jdbc.SQLServerDriver";
	ResultSet rs=null;
	PreparedStatement ps =null;
	//2、定义操作数据库的方法：增、删、改、查
	//（1）数据增、删、改方法
	public boolean updateExecute(String sql, String[] paras){
		boolean result= false;
		try{
			//1、加载驱动
			Class.forName(driver);
			//2、获取连接对象
			con = DriverManager.getConnection(dbUrl, user, password);
			//3、创建ps
			ps=con.prepareStatement(sql);
			//4、处理参数
			if(paras !=null){
				for(int i=0;i<paras.length;i++){
					ps.setString(i+1, paras[i]);
				}
			}
			//5、执行操作
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
	
	//（2）数据查询方法
	public ResultSet queryExecute(String sql, String[] paras){
		try{
			//1、加载驱动
			Class.forName(driver);
			//2、获取连接对象
			con = DriverManager.getConnection(dbUrl, user, password);
			//3、创建ps
			ps=con.prepareStatement(sql);
			//4、处理参数
			if(paras !=null){
				for(int i=0;i<paras.length;i++){
					ps.setString(i+1, paras[i]);
				}
			}
			//5、执行操作
			 rs= ps.executeQuery();
		}catch(Exception e){
			e.printStackTrace();
		}
		return rs;
	}
	
}
