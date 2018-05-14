		$(function(){
					var data = [
					        	{name : '电子商务',value : 100,color:'#a5c2d5'},
					        	{name : '市场营销',value : 10,color:'#cbab4f'},
					        	{name : '网页设计',value : 15,color:'#76a871'},
					        	{name : '心理健康',value : 10,color:'#9f7961'},
					        	{name : '大学英语',value : 10,color:'#a56f8f'}
				        	];
		        	
					var chart = new iChart.Column2D({
						render : 'c',
						data: data,
						title : 'strength成绩',
						width : 360,
						height : 400,
						coordinate:{
							width:300,
							height:260,
							scale:[{
								 position:'left',	
								 start_scale:0,
								 end_scale:100,
								 scale_space:10
							}]
						}
					});

					/**
					 *自定义组件,画矩形区域。
					 */
					chart.plugin(new iChart.Custom({
							drawFn:function(){
								/**
								 *计算平均值的高度(坐标Y值)
								 */	
								var avg = chart.total/5,
									coo = chart.getCoordinate(),
									x = coo.get('originx'),
									W = coo.width,
									S = coo.getScale('left'),
									H = coo.height,
									h = (avg - S.start) * H / S.distance,
									y = chart.y + H - h;

								chart.target.globalAlpha(0.2)
								.box(x,y,W,h,0,'#1f7e92')
								.globalAlpha(1)
								.textAlign('start')
								.textBaseline('middle')
								.textFont('600 12px Verdana')
						
								
							}
					}));	
						
					chart.draw();
			});

				$(function(){
					var pp = [
					        	{name : '网络广告',value : 53,color:'#a5c2d5'},
					        	{name : '网络营销',value : 80,color:'#cbab4f'},
					        	{name : '创业实务',value : 60,color:'#76a871'},
					        	{name : '推销谈判',value : 18,color:'#9f7961'},
					        	{name : '策划实训',value : 12,color:'#a56f8f'}
				        	];
		        	
					var chart = new iChart.Column2D({
						render : 'd',
						data: pp,
						title : 'weakness成绩',
						width : 360,
						height : 400,
						coordinate:{
							width:250,
							height:260,
							scale:[{
								 position:'left',	
								 start_scale:0,
								 end_scale:100,
								 scale_space:10
							}]
						}
					});

					/**
					 *自定义组件,画矩形区域。
					 */
					chart.plugin(new iChart.Custom({
							drawFn:function(){
								/**
								 *计算平均值的高度(坐标Y值)
								 */	
								var avg = chart.total/5,
									coo = chart.getCoordinate(),
									x = coo.get('originx'),
									W = coo.width,
									S = coo.getScale('left'),
									H = coo.height,
									h = (avg - S.start) * H / S.distance,
									y = chart.y + H - h;

								chart.target.globalAlpha(0.2)
								.box(x,y,W,h,0,'#1f7e92')
								.globalAlpha(1)
								.textAlign('start')
								.textBaseline('middle')
								.textFont('600 12px Verdana')
						
								
							}
					}));	
						
					chart.draw();
			});

		//定义数据
		var ta = [
			{name : '阅读',value : 7,color:'#a5c2d5'},
		   	{name : '写作',value : 5,color:'#cbab4f'},
		   	{name : '演讲',value : 12,color:'#76a871'},
		   	{name : '才艺',value : 12,color:'#76a871'},
		   	{name : '竞赛',value : 15,color:'#a56f8f'},
		   	{name : '沟通',value : 13,color:'#c12c44'},
		   	{name : '出勤',value : 15,color:'#a56f8f'},
		   	{name : '实践',value : 18,color:'#9f7961'}

		 ];
		 $(function(){	
			var chart = new iChart.Column2D({
				render : 'shuxin',//渲染的Dom目标,canvasDiv为Dom的ID
				data: ta,//绑定数据
				title : '属性',//设置标题
				width : 320,//设置宽度，默认单位为px
				height : 400,//设置高度，默认单位为px
				shadow:true,//激活阴影
				shadow_color:'#c7c7c7',//设置阴影颜色
				coordinate:{//配置自定义坐标轴
					scale:[{//配置自定义值轴
						 position:'left',//配置左值轴	
						 start_scale:0,//设置开始刻度为0
						 end_scale:100,//设置结束刻度为26
						 scale_space:10,//设置刻度间距
						 listeners:{//配置事件
							parseText:function(t,x,y){//设置解析值轴文本
								return {text:t}
							}
						}
					}]
				}
			});
			//调用绘图方法开始绘图
			chart.draw();
		});