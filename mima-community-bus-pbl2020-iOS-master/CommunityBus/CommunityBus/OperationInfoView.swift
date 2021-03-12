//
//  OperationInfoView.swift
//  CommunityBus
//
//  Created by KomoriSoto on 2020/09/07.
//  Copyright © 2020 EhimeUniversity. All rights reserved.
//

import SwiftUI

var routeId:String = "1"
var routeOrderId:String = "1"
var selectedCourse = 0
//コースに含まれる路線の数
var numberOfRoute = 0
//バス停一覧を格納
var busStops: Array<Dictionary<String, String>> = [[:]]
//コースに含まれる路線の数
var numberOfCourseRoute = 0

struct OperationInfoView: View {
    @State var isActiveCountBoardingsView = false
    @State var isActiveLoginView = false
    @State var isActiveFinishOperationView = false
    @Binding var isActiveOperationInitialSettingView: Bool
    @State var selectedRoute = 0
    @State var selectedRouteOrder = 0
    @State var showingLogoutAlert = false
    @State var showingFinishAlert = false
    @State var showingErrorAlert = false
    @State var courseSelections = Courses()
    @State var route = ""
    @State var routeOrder = ""
    @State var cannotGetCourseAlert = false
    @State var cannotLogoutError = false
    @State var routes:[String] = []
    @State var routeOrders: [String] = []
    @State var changeFlag = false
    @State var apiErrorAlert = false
    @State var isFirst = true
    
    var fontSize = 25
    
    
    var body: some View {
        ZStack {
            Color.gray.opacity(0.1)
                .edgesIgnoringSafeArea(.all)
            VStack() {
                NavigationLink(destination: LoginView(),
                               isActive: $isActiveLoginView) {
                    EmptyView()
                }
                //コード上のイベントで遷移したい場合は、LabelにEmptyViewを指定する
                NavigationLink(destination: CountBoardingsView(isActiveOperationInitialSettingView: $isActiveOperationInitialSettingView, isActiveCountBoardingsView: $isActiveCountBoardingsView, route: self.$route, routeOrder: self.$routeOrder),
                               isActive: $isActiveCountBoardingsView) {
                    EmptyView()
                }.isDetailLink(false)
                .navigationBarTitle("運行情報入力画面", displayMode: .inline)
                NavigationLink(destination: FinishOperationView(isActiveOperationInitialSettingView: $isActiveOperationInitialSettingView),
                               isActive: $isActiveFinishOperationView) {
                    EmptyView()
                }.isDetailLink(false)
                .navigationBarTitle("運行情報入力画面", displayMode: .inline)
                .onAppear {
                    do{
                        //                        コース情報を取得
                        let api = CallAPI.init()
                        let CourseDict:[String: String] = [
                            "course_id": course_id
                        ]
                        if monitor.currentPath.status == .unsatisfied{
                            throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                        }
                        let jsonDataCourse = api.requestData(url: "/bus/course/info/", dict: CourseDict, type: "POST")
                        if apiErrorFlag == true{
                            apiErrorAlert = true
                            apiErrorFlag = false
                            throw NSError(domain: "errorメッセージ", code: -1, userInfo: nil)
                        }
                        self.courseSelections = try JSONDecoder().decode(Courses.self, from: jsonDataCourse)
                        
                        numberOfCourseRoute = Int(self.courseSelections.course.count)
                        if numberOfCourseRoute == 0 {
                            self.cannotGetCourseAlert = true
                        }
                        
                        //                        コースに含まれている路線のリストを作成
                        for i in 0..<numberOfCourseRoute{
                            self.routes.append(getRouteNameFromCourse(courseInfo: self.courseSelections.course[i]))
                        }
                        
                        //                        リストから重複を削除
                        self.routes = routes.reduce([], { $0.contains($1) ? $0 : $0 + [$1] })
                        
                        //                        便のリストを作成
                        self.routeOrders = []
                        for i in 0..<numberOfCourseRoute{
                            if self.routes[selectedRoute] == getRouteNameFromCourse(courseInfo: self.courseSelections.course[i]){
                                self.routeOrders.append(getRouteOrderNameFromCourse(courseInfo: self.courseSelections.course[i]))
                            }
                        }
                        
                        if !changeFlag {
                            //                            便・路線の更新
                            self.route = getRouteNameFromCourse(courseInfo: self.courseSelections.course[selectedCourse])
                            self.routeOrder = getRouteOrderNameFromCourse(courseInfo: self.courseSelections.course[selectedCourse])
                            //                            路線の選択
                            for i in 0..<self.routes.count{
                                if self.route == routes[i]{
                                    self.isFirst = true
                                    self.selectedRoute = i
                                }
                            }
                            
                            //                        便のリストを作成
                            self.routeOrders = []
                            for i in 0..<numberOfCourseRoute{
                                if self.routes[selectedRoute] == getRouteNameFromCourse(courseInfo: self.courseSelections.course[i]){
                                    self.routeOrders.append(getRouteOrderNameFromCourse(courseInfo: self.courseSelections.course[i]))
                                }
                            }
                            
                            //                            便の選択
                            for i in 0..<routeOrders.count{
                                if self.routeOrder == routeOrders[i]{
                                    self.selectedRouteOrder = i
                                }
                            }
                            self.changeFlag = true
                        }
                    }catch {
                        if self.apiErrorAlert == false{
                            cannotGetCourseAlert = true
                        }
                    }
                }.alert(isPresented: self.$cannotGetCourseAlert) {
                    Alert(
                        title: Text("通信エラー"),
                        message: Text("コース情報の取得に失敗しました")
                    )
                }
                .navigationBarBackButtonHidden(true)
                Text("")
                .alert(isPresented: $apiErrorAlert){
                    Alert(
                        title: Text("送信に失敗しました"),
                        message: Text("もう一度お試しください")
                    )
                }
                Form {
                    Section(header: Text("運行便確認（異なる場合は変更してください）")                    .font(.system(size: CGFloat(self.fontSize)))) {
                        //                        路線名のリストを動的に生成
                        Picker(selection: $selectedRoute,
                               label: Text("路線")
                                .font(.system(size: CGFloat(self.fontSize))))
                        {
                            ForEach(0 ..< routes.count, id: \.self){ i in
                                Text(routes[i])
                                    .font(.system(size: CGFloat(self.fontSize)))
                            }
                        }.onChange(of: self.selectedRoute, perform: { value in
                            self.route = self.routes[selectedRoute]
                            self.routeOrders = []
                            for i in 0..<numberOfCourseRoute{
                                if self.route == getRouteNameFromCourse(courseInfo: self.courseSelections.course[i]){
                                    self.routeOrders.append(getRouteOrderNameFromCourse(courseInfo: self.courseSelections.course[i]))
                                }
                            }
                            self.routeOrder = self.routeOrders[0]
                            if(isFirst){
                                self.routeOrder = getRouteOrderNameFromCourse(courseInfo: self.courseSelections.course[selectedCourse])
                                isFirst = false
                            }
                        })
                        
                        Picker(selection: $selectedRouteOrder,
                               label: Text("便")                    .font(.system(size: CGFloat(self.fontSize))))
                        {
                            //                            便のリストを動的に生成．便数は選択されている路線に応じて動的に変化する
                            ForEach(0..<routeOrders.count, id: \.self) {i in
                                Text(routeOrders[i])
                                    .font(.system(size: CGFloat(self.fontSize)))
                            }
                        }.onChange(of: self.selectedRouteOrder, perform: { value in
                            self.routeOrder = self.routeOrders[selectedRouteOrder]
                        })
                        Button(action: {
                            for i in 0..<numberOfCourseRoute{
                                if self.route == getRouteNameFromCourse(courseInfo: self.courseSelections.course[i]) && self.routeOrder == getRouteOrderNameFromCourse(courseInfo: self.courseSelections.course[i]){
                                    selectedCourse = i
                                    busStops = getBusStopsFromCourse(courseInfo: self.courseSelections.course[selectedCourse])
                                    routeId = courseSelections.course[selectedCourse].route_id
                                    routeOrderId = courseSelections.course[selectedCourse].route_order_id
                                    break
                                }
                            }
                            self.changeFlag = false
                            self.isActiveCountBoardingsView.toggle()
                        },
                        label: {
                            Text("運行開始")
                                .font(.system(size: CGFloat(self.fontSize)))
                        })
                    }
                    
                    //                    空白スペースの追加
                    Section(header: Text("")) {
                        EmptyView()
                    }.padding(.bottom, UIScreen.main.bounds.height * 1/2)
                    
                    Section(){
                        Button(action: {
                            self.isActiveFinishOperationView.toggle()
                            
                        })
                        {
                            Text("本日の業務終了")
                                .font(.system(size: CGFloat(self.fontSize)))
                                .foregroundColor(Color.red)
                        }
                    }
                }
            }.frame(maxWidth: UIScreen.main.bounds.width * 4 / 5)
        }
    }
    
    /// 路線名の取得．CourseInfo型の情報(courseSelections.course[i])を受け取って，CourseInfoの中にあるroute_name（路線名）をリターンする
    /// - Parameters:
    ///   - CourseInfo:路線に関する情報．CourseInfo型
    /// - Returns: CourseInfoの中にあるroute_name（路線名）
    func getRouteNameFromCourse(courseInfo:CourseInfo) -> String{
        let course = courseInfo as AnyObject? as! CourseInfo
        return course.route_name
    }
    
    
    /// 便名の取得．CourseInfo型の情報(courseSelections.course[i])を受け取って，CourseInfoの中にあるroute_order_name（第何便か）をリターンする
    /// - Parameters:
    ///   - CourseInfo:路線に関する情報．CourseInfo型
    /// - Returns: CourseInfoの中にあるroute_order_name（便名）
    func getRouteOrderNameFromCourse(courseInfo:CourseInfo) -> String{
        let order = courseInfo as AnyObject? as! CourseInfo
        return order.route_order_name
    }
    
    /// 停留所一覧の取得．CourseInfo型の情報(courseSelections.course[i])を受け取って，CourseInfoの中にあるbus_stops（停留所一覧）をリターンする
    /// - Parameters:
    ///   - courseInfo:コースに関する情報．CourseInfo型
    /// - Returns: CourseInfoの中にあるbus_stops（停留所一覧）
    func getBusStopsFromCourse(courseInfo:CourseInfo) -> Array<Dictionary<String,String>>{
        let bus_Stops = courseInfo as AnyObject? as! CourseInfo
        return bus_Stops.bus_stops
    }
}

struct Courses: Codable {
    var course: [CourseInfo] = [CourseInfo()]
}

struct CourseInfo: Codable {
    var route_id: String = ""
    var route_name: String = ""
    var route_order_id: String = ""
    var route_order_name: String = ""
    var bus_stops: Array<Dictionary<String,String>> = []
}
