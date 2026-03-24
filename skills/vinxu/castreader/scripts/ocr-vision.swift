#!/usr/bin/env swift
// Apple Vision Framework OCR CLI
// Usage: swift ocr-vision.swift <image_path>
// Outputs recognized text to stdout

import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count > 1 else {
    fputs("Usage: ocr-vision <image_path>\n", stderr)
    exit(1)
}

let imagePath = CommandLine.arguments[1]
guard let image = NSImage(contentsOfFile: imagePath),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    fputs("Error: Cannot load image: \(imagePath)\n", stderr)
    exit(1)
}

let semaphore = DispatchSemaphore(value: 0)
var resultText = ""

let request = VNRecognizeTextRequest { request, error in
    if let error = error {
        fputs("Error: \(error.localizedDescription)\n", stderr)
        semaphore.signal()
        return
    }
    guard let observations = request.results as? [VNRecognizedTextObservation] else {
        semaphore.signal()
        return
    }
    // Sort by vertical position (top to bottom)
    let sorted = observations.sorted { $0.boundingBox.origin.y > $1.boundingBox.origin.y }
    resultText = sorted.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
    semaphore.signal()
}

request.recognitionLevel = .accurate
request.recognitionLanguages = ["en-US"]
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])
semaphore.wait()

print(resultText)
