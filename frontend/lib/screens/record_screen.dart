import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import '../services/audio_service.dart';
import '../services/api_service.dart';
import 'dart:async';

final audioServiceProvider = Provider((ref) => AudioService());

class RecordScreen extends ConsumerStatefulWidget {
  const RecordScreen({super.key});

  @override
  ConsumerState<RecordScreen> createState() => _RecordScreenState();
}

class _RecordScreenState extends ConsumerState<RecordScreen> {
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  bool _isRecording = false;
  bool _isUploading = false;
  String? _recordedFilePath;
  String? _selectedFilePath;
  int _recordingSeconds = 0;
  Timer? _timer;

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    _timer?.cancel();
    super.dispose();
  }

  void _startTimer() {
    _recordingSeconds = 0;
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted) {
        setState(() {
          _recordingSeconds++;
        });
      }
    });
  }

  void _stopTimer() {
    _timer?.cancel();
    _timer = null;
  }

  Future<void> _startRecording() async {
    final audioService = ref.read(audioServiceProvider);

    try {
      await audioService.startRecording();
      setState(() {
        _isRecording = true;
        _recordedFilePath = null;
        _selectedFilePath = null;
      });
      _startTimer();
    } catch (e) {
      _showError('Failed to start recording: $e');
    }
  }

  Future<void> _stopRecording() async {
    final audioService = ref.read(audioServiceProvider);

    try {
      final path = await audioService.stopRecording();
      _stopTimer();
      setState(() {
        _isRecording = false;
        _recordedFilePath = path;
      });
    } catch (e) {
      _showError('Failed to stop recording: $e');
    }
  }

  Future<void> _cancelRecording() async {
    final audioService = ref.read(audioServiceProvider);

    try {
      await audioService.cancelRecording();
      _stopTimer();
      setState(() {
        _isRecording = false;
        _recordedFilePath = null;
        _recordingSeconds = 0;
      });
    } catch (e) {
      _showError('Failed to cancel recording: $e');
    }
  }

  Future<void> _pickFile() async {
    try {
      final result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm'],
      );

      if (result != null && result.files.single.path != null) {
        setState(() {
          _selectedFilePath = result.files.single.path;
          _recordedFilePath = null;
        });
      }
    } catch (e) {
      _showError('Failed to pick file: $e');
    }
  }

  Future<void> _uploadMeeting() async {
    final filePath = _recordedFilePath ?? _selectedFilePath;

    if (filePath == null) {
      _showError('No audio file selected');
      return;
    }

    if (_titleController.text.trim().isEmpty) {
      _showError('Please enter a meeting title');
      return;
    }

    setState(() {
      _isUploading = true;
    });

    try {
      final apiService = ref.read(ApiServiceProvider);
      await apiService.createMeeting(
        title: _titleController.text.trim(),
        description: _descriptionController.text.trim().isEmpty
            ? null
            : _descriptionController.text.trim(),
        audioFile: File(filePath),
        language: 'id',
        useIndonesianModel: true,
      );

      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Meeting uploaded successfully!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      _showError('Failed to upload meeting: $e');
    } finally {
      if (mounted) {
        setState(() {
          _isUploading = false;
        });
      }
    }
  }

  void _showError(String message) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  String _formatDuration(int seconds) {
    final minutes = seconds ~/ 60;
    final secs = seconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final hasAudio = _recordedFilePath != null || _selectedFilePath != null;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Record Meeting'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Recording Controls
            Card(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    if (_isRecording) ...[
                      const Icon(
                        Icons.mic,
                        size: 80,
                        color: Colors.red,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'Recording...',
                        style: Theme.of(context).textTheme.headlineSmall,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        _formatDuration(_recordingSeconds),
                        style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                              color: Colors.red,
                              fontWeight: FontWeight.bold,
                            ),
                      ),
                      const SizedBox(height: 24),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          ElevatedButton.icon(
                            onPressed: _cancelRecording,
                            icon: const Icon(Icons.close),
                            label: const Text('Cancel'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.grey,
                            ),
                          ),
                          ElevatedButton.icon(
                            onPressed: _stopRecording,
                            icon: const Icon(Icons.stop),
                            label: const Text('Stop'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.red,
                            ),
                          ),
                        ],
                      ),
                    ] else ...[
                      Icon(
                        hasAudio ? Icons.check_circle : Icons.mic_none,
                        size: 80,
                        color: hasAudio ? Colors.green : Colors.grey,
                      ),
                      const SizedBox(height: 16),
                      if (hasAudio) ...[
                        Text(
                          'Audio Ready',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          _recordedFilePath != null
                              ? 'Recorded: ${_formatDuration(_recordingSeconds)}'
                              : 'File selected',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: Colors.grey,
                              ),
                        ),
                        const SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: _startRecording,
                          icon: const Icon(Icons.mic),
                          label: const Text('Record Again'),
                        ),
                      ] else ...[
                        Text(
                          'Ready to Record',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: _startRecording,
                          icon: const Icon(Icons.mic),
                          label: const Text('Start Recording'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 32,
                              vertical: 16,
                            ),
                          ),
                        ),
                      ],
                      const SizedBox(height: 16),
                      const Text('or'),
                      const SizedBox(height: 16),
                      OutlinedButton.icon(
                        onPressed: _pickFile,
                        icon: const Icon(Icons.file_upload),
                        label: const Text('Upload Audio File'),
                      ),
                    ],
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Meeting Details
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(
                labelText: 'Meeting Title',
                hintText: 'Enter meeting title',
                prefixIcon: Icon(Icons.title),
              ),
              enabled: !_isUploading && !_isRecording,
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _descriptionController,
              decoration: const InputDecoration(
                labelText: 'Description (Optional)',
                hintText: 'Enter meeting description',
                prefixIcon: Icon(Icons.description),
              ),
              maxLines: 3,
              enabled: !_isUploading && !_isRecording,
            ),
            const SizedBox(height: 24),

            // Upload Button
            ElevatedButton.icon(
              onPressed: hasAudio && !_isUploading && !_isRecording
                  ? _uploadMeeting
                  : null,
              icon: _isUploading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation(Colors.white),
                      ),
                    )
                  : const Icon(Icons.cloud_upload),
              label: Text(_isUploading ? 'Uploading...' : 'Upload & Transcribe'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.all(16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// Provider fix
final ApiServiceProvider = Provider((ref) => ApiService());
