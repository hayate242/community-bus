import Foundation

var apiErrorFlag = false

class CallAPI {
    
    private var baseUrl: String
    init() {
        
////                モックサーバーを使う場合のurl
//                self.baseUrl = "http://ictx01.ict.ehime-u.ac.jp:3000/api/v1"
        
//                本番環境用のurl
        self.baseUrl = "http://b-map.pbl.jp:80/api/v1"

    }
    
    /// urlで指定したAPIから情報を取得or送信
    /// - seeAlso: "https://github.com/ictc/mima-community-bus-pbl-api"
    /// - Parameters:
    ///   - url:"http://ictx01.ict.ehime-u.ac.jp:3000"以下のパス．<例>"/user/info"
    ///   - body:body（bodyが必要であれば入力），なければ [:]を入力
    ///   - type:通信方式を選択（POSTの場合は”POST”，GETの場合は"GET"
    /// - Returns: APImockサーバーで設定された情報．
    func requestData(url:String, dict: Dictionary<String,Any>, type:String) -> Data{
        
        var json: String = ""
        do {
            // Dict -> JSON
            let jsonData = try JSONSerialization.data(withJSONObject: dict, options: []) //(*)options??
            json = NSString(data: jsonData, encoding: String.Encoding.utf8.rawValue)! as String
        } catch {
            print("Error!: \(error)")
            return Data()
        }
        let semaphore = DispatchSemaphore(value: 0)
        var result = ""
        var request = URLRequest(url: URL(string: baseUrl + url)!)
        if(type == "POST"){
            request.httpMethod = "POST"
            if(json != "" && json != "{}"){
                // POSTするデータをBodyとして設定
                request.httpBody = json.data(using: .utf8)
            }
        }
        
        let jsonDataToken = UserDefaults.standard.data(forKey: "token")
        let token = try? JSONDecoder().decode(Token.self, from: jsonDataToken!)
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer " + token!.access_token , forHTTPHeaderField: "Authorization")
        let session = URLSession.shared
        
        session.dataTask(with: request) { (data, response, error) in
            if error != nil{
                apiErrorFlag = true
                // 処理終了でセマフォをインクリメント
                semaphore.signal()
            }
            if error == nil, let data = data, let response = response as? HTTPURLResponse {
                // HTTPヘッダの取得
                print("Content-Type: \(response.allHeaderFields["Content-Type"] ?? "")")
                // HTTPステータスコード
                print("statusCode: \(response.statusCode)")
                print(String(data: data, encoding: String.Encoding.utf8) ?? "")
                result = String(data: data, encoding: String.Encoding.utf8) ?? ""
                // 処理終了でセマフォをインクリメント
                semaphore.signal()
            }
        }.resume()
        
        // セマフォをデクリメントして待つ
        semaphore.wait()
        
        //            json文字列をdict型に変換
        return result.data(using: .utf8)!
    }
    
}


