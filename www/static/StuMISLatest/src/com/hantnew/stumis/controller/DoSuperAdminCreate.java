package com.hantnew.stumis.controller;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.hantnew.stumis.domain.SuperAdmin;
import com.hantnew.stumis.service.SuperAdminService;
import com.hantnew.stumis.serviceimpl.SuperAdminServiceImpl;
import com.hantnew.stumis.viewmodel.SuperAdminViewModel;

/**
 * Servlet implementation class DoSuperAdminCreate
 */
@WebServlet("/DoSuperAdminCreate")
public class DoSuperAdminCreate extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public DoSuperAdminCreate() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		SuperAdminViewModel viewModel = new SuperAdminViewModel();
		SuperAdminService service = new SuperAdminServiceImpl();
		// TODO Auto-generated method stub
		//response.getWriter().append("Served at: ").append(request.getContextPath());
	    //1、获取用户提交的数据
		String userName=request.getParameter("userNameInput");
		String password=request.getParameter("passwordInput");
		String repeatPassword=request.getParameter("repeatPasswordInput");
		viewModel.setUserName(userName);
		viewModel.setPassword(password);
		viewModel.setRepeatePassword(repeatPassword);
		//2、判断验证是否通过
		if(!viewModel.validate()){
			//如果验证不通过，则跳转到用户创建页
			request.setAttribute("myData", viewModel);
			request.getRequestDispatcher("/WEB-INF/SuperAdmin/Create.jsp").forward(request, response);
		
		}else{
			try{
				SuperAdmin superAdmin = new SuperAdmin();
				superAdmin.setUserName(userName);
				superAdmin.setPassword(password);
				if( service.add(superAdmin))
				{
					request.getRequestDispatcher("/WEB-INF/SuperAdmin/CreateSuccess.jsp").forward(request, response);
				}else{
					request.getRequestDispatcher("/WEB-INF/SuperAdmin/CreateFail.jsp").forward(request, response);
				}
				
			}catch(Exception e){
				request.getRequestDispatcher("/WEB-INF/SuperAdmin/CreateFail.jsp").forward(request, response);
				e.printStackTrace();
			}
		}
	
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
