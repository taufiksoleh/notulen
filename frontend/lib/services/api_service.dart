import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import '../models/meeting.dart';

class ApiService {
  final String baseUrl;

  ApiService({this.baseUrl = 'http://localhost:8000/api/v1'});

  /// Check API health
  Future<Map<String, dynamic>> healthCheck() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Health check failed: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to connect to API: $e');
    }
  }

  /// Upload audio file and create meeting
  Future<Meeting> createMeeting({
    required String title,
    String? description,
    required File audioFile,
    String language = 'id',
    bool useIndonesianModel = true,
  }) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/meetings'),
      );

      // Add fields
      request.fields['title'] = title;
      if (description != null) {
        request.fields['description'] = description;
      }
      request.fields['language'] = language;
      request.fields['use_indonesian_model'] = useIndonesianModel.toString();

      // Add file
      var audioStream = http.ByteStream(audioFile.openRead());
      var audioLength = await audioFile.length();
      var multipartFile = http.MultipartFile(
        'audio_file',
        audioStream,
        audioLength,
        filename: audioFile.path.split('/').last,
        contentType: MediaType('audio', _getAudioType(audioFile.path)),
      );
      request.files.add(multipartFile);

      // Send request
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return Meeting.fromJson(jsonData);
      } else {
        throw Exception('Failed to create meeting: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error creating meeting: $e');
    }
  }

  /// Get all meetings
  Future<List<Meeting>> getMeetings({int skip = 0, int limit = 100}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/meetings?skip=$skip&limit=$limit'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> jsonData = json.decode(response.body);
        return jsonData.map((json) => Meeting.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load meetings: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error loading meetings: $e');
    }
  }

  /// Get a specific meeting
  Future<Meeting> getMeeting(int meetingId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/meetings/$meetingId'),
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return Meeting.fromJson(jsonData);
      } else if (response.statusCode == 404) {
        throw Exception('Meeting not found');
      } else {
        throw Exception('Failed to load meeting: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error loading meeting: $e');
    }
  }

  /// Delete a meeting
  Future<void> deleteMeeting(int meetingId) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/meetings/$meetingId'),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to delete meeting: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error deleting meeting: $e');
    }
  }

  /// Regenerate summary for a meeting
  Future<Meeting> regenerateSummary(int meetingId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/meetings/$meetingId/regenerate-summary'),
      );

      if (response.statusCode == 200) {
        final jsonData = json.decode(response.body);
        return Meeting.fromJson(jsonData);
      } else {
        throw Exception('Failed to regenerate summary: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error regenerating summary: $e');
    }
  }

  String _getAudioType(String filename) {
    final extension = filename.split('.').last.toLowerCase();
    switch (extension) {
      case 'mp3':
        return 'mpeg';
      case 'wav':
        return 'wav';
      case 'm4a':
        return 'm4a';
      case 'ogg':
        return 'ogg';
      case 'flac':
        return 'flac';
      case 'webm':
        return 'webm';
      default:
        return 'mpeg';
    }
  }
}
