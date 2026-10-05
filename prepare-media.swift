import Foundation
import AVFoundation
import AppKit
let root = URL(fileURLWithPath: CommandLine.arguments[1])
let dest = URL(fileURLWithPath: CommandLine.arguments[2])
let files = [("video_codem-camions-route-.mp4","route"),("video_codem-entreprises-5s.mp4","entreprises"),("video_codem-particuliers.mp4","particuliers"),("video_codem-piano.mp4","piano")]
for (file,name) in files {
 let asset = AVURLAsset(url:root.appendingPathComponent(file))
 let gen=AVAssetImageGenerator(asset:asset); gen.appliesPreferredTrackTransform=true
 let img=try gen.copyCGImage(at:.zero,actualTime:nil)
 try NSBitmapImageRep(cgImage:img).representation(using:.jpeg,properties:[.compressionFactor:0.85])!.write(to:dest.appendingPathComponent(name+"-poster.jpg"))
 let export=AVAssetExportSession(asset:asset,presetName:AVAssetExportPreset1280x720)!
 export.outputURL=dest.appendingPathComponent(name+".mp4"); export.outputFileType = .mp4; export.shouldOptimizeForNetworkUse=true
 let sem=DispatchSemaphore(value:0); export.exportAsynchronously { sem.signal() }; sem.wait()
 print(name,export.status.rawValue)
}
