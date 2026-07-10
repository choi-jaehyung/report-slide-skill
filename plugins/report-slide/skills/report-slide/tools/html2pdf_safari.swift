import Cocoa
import WebKit
import PDFKit

let args = CommandLine.arguments
guard args.count >= 5 else {
    print("usage: html2pdf_safari <input.html> <output.pdf> <slideCount> <slideHeight>")
    exit(1)
}
let inputPath = args[1]
let outputPath = args[2]
let slideCount = Int(args[3])!
let slideHeight = Double(args[4])!
let slideWidth = 1280.0

let inputURL = URL(fileURLWithPath: inputPath)
let outputURL = URL(fileURLWithPath: outputPath)

let app = NSApplication.shared

class Delegate: NSObject, WKNavigationDelegate {
    let webView: WKWebView
    let outputURL: URL
    let slideCount: Int
    let slideHeight: Double
    let slideWidth: Double
    var pageDatas: [Data?] = []

    init(webView: WKWebView, outputURL: URL, slideCount: Int, slideHeight: Double, slideWidth: Double) {
        self.webView = webView
        self.outputURL = outputURL
        self.slideCount = slideCount
        self.slideHeight = slideHeight
        self.slideWidth = slideWidth
        self.pageDatas = Array(repeating: nil, count: slideCount)
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
            self.captureNext(index: 0)
        }
    }

    func captureNext(index: Int) {
        if index >= slideCount {
            finish()
            return
        }
        let rect = CGRect(x: 0, y: Double(index) * slideHeight, width: slideWidth, height: slideHeight)
        let config = WKPDFConfiguration()
        config.rect = rect
        webView.createPDF(configuration: config) { result in
            switch result {
            case .success(let data):
                self.pageDatas[index] = data
            case .failure(let error):
                print("page \(index) failed: \(error)")
            }
            self.captureNext(index: index + 1)
        }
    }

    func finish() {
        let combined = PDFDocument()
        for (i, data) in pageDatas.enumerated() {
            guard let data = data, let single = PDFDocument(data: data), let page = single.page(at: 0) else {
                print("missing page \(i)")
                continue
            }
            combined.insert(page, at: combined.pageCount)
        }
        if combined.write(to: outputURL) {
            print("wrote \(combined.pageCount) pages to \(outputURL.path)")
        } else {
            print("failed to write combined pdf")
        }
        exit(0)
    }
}

let webView = WKWebView(frame: NSRect(x: 0, y: 0, width: 1280, height: 800))
let delegate = Delegate(webView: webView, outputURL: outputURL, slideCount: slideCount, slideHeight: slideHeight, slideWidth: slideWidth)
webView.navigationDelegate = delegate
webView.loadFileURL(inputURL, allowingReadAccessTo: inputURL.deletingLastPathComponent())

app.run()
