#!/usr/bin/env swift
// Apple Vision Framework OCR — Batch mode
// Usage: ocr-vision-batch <dir_with_pngs>
// Processes all page-*.png files in order, outputs JSON array of texts

import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count > 1 else {
    fputs("Usage: ocr-vision-batch <directory>\n", stderr)
    exit(1)
}

let dirPath = CommandLine.arguments[1]
let fm = FileManager.default

// Find all page-*.png files, sorted
guard let files = try? fm.contentsOfDirectory(atPath: dirPath) else {
    fputs("Error: Cannot read directory: \(dirPath)\n", stderr)
    exit(1)
}

let pageFiles = files.filter { $0.hasPrefix("page-") && $0.hasSuffix(".png") }.sorted()
if pageFiles.isEmpty {
    fputs("Error: No page-*.png files found in \(dirPath)\n", stderr)
    exit(1)
}

fputs("Processing \(pageFiles.count) pages...\n", stderr)
let startTime = Date()

var results: [String] = []
var processedCount = 0

for fileName in pageFiles {
    let filePath = (dirPath as NSString).appendingPathComponent(fileName)

    guard let image = NSImage(contentsOfFile: filePath),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        results.append("")
        continue
    }

    let semaphore = DispatchSemaphore(value: 0)
    var pageText = ""

    let request = VNRecognizeTextRequest { request, error in
        defer { semaphore.signal() }
        guard error == nil,
              let observations = request.results as? [VNRecognizedTextObservation] else { return }
        let sorted = observations.sorted { $0.boundingBox.origin.y > $1.boundingBox.origin.y }
        pageText = sorted.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
    }

    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["en-US"]
    request.usesLanguageCorrection = true

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try? handler.perform([request])
    semaphore.wait()

    results.append(pageText)
    processedCount += 1

    if processedCount % 50 == 0 {
        fputs("  \(processedCount)/\(pageFiles.count) pages\n", stderr)
    }
}

let elapsed = Date().timeIntervalSince(startTime)
fputs("Done: \(pageFiles.count) pages in \(String(format: "%.1f", elapsed))s (\(String(format: "%.0f", elapsed / Double(pageFiles.count) * 1000))ms/page)\n", stderr)

// Output as JSON array
let jsonData = try! JSONSerialization.data(withJSONObject: results, options: [])
print(String(data: jsonData, encoding: .utf8)!)
