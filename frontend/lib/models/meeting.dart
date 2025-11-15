import 'package:json_annotation/json_annotation.dart';

part 'meeting.g.dart';

@JsonSerializable()
class Meeting {
  final int id;
  final String title;
  final String? description;
  final String audioFilePath;
  final double? audioDuration;
  final String? transcription;
  final List<TranscriptionSegment>? transcriptionSegments;
  final String? detectedLanguage;
  final String? modelUsed;
  final String? summary;
  final List<String>? actionItems;
  final List<String>? keyPoints;
  final String status;
  final String? errorMessage;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final DateTime? processedAt;

  Meeting({
    required this.id,
    required this.title,
    this.description,
    required this.audioFilePath,
    this.audioDuration,
    this.transcription,
    this.transcriptionSegments,
    this.detectedLanguage,
    this.modelUsed,
    this.summary,
    this.actionItems,
    this.keyPoints,
    required this.status,
    this.errorMessage,
    required this.createdAt,
    this.updatedAt,
    this.processedAt,
  });

  factory Meeting.fromJson(Map<String, dynamic> json) => _$MeetingFromJson(json);
  Map<String, dynamic> toJson() => _$MeetingToJson(this);

  String get formattedDuration {
    if (audioDuration == null) return 'Unknown';
    final minutes = (audioDuration! / 60).floor();
    final seconds = (audioDuration! % 60).floor();
    return '$minutes:${seconds.toString().padLeft(2, '0')}';
  }

  bool get isProcessing => status == 'processing';
  bool get isCompleted => status == 'completed';
  bool get isFailed => status == 'failed';
}

@JsonSerializable()
class TranscriptionSegment {
  final double start;
  final double end;
  final String text;

  TranscriptionSegment({
    required this.start,
    required this.end,
    required this.text,
  });

  factory TranscriptionSegment.fromJson(Map<String, dynamic> json) =>
      _$TranscriptionSegmentFromJson(json);
  Map<String, dynamic> toJson() => _$TranscriptionSegmentToJson(this);

  String get timeRange {
    final startMin = (start / 60).floor();
    final startSec = (start % 60).floor();
    final endMin = (end / 60).floor();
    final endSec = (end % 60).floor();
    return '$startMin:${startSec.toString().padLeft(2, '0')} - $endMin:${endSec.toString().padLeft(2, '0')}';
  }
}
