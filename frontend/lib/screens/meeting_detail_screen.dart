import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/meeting.dart';
import '../services/api_service.dart';

// Provider for a specific meeting
final meetingProvider = FutureProvider.family<Meeting, int>((ref, meetingId) async {
  final apiService = ref.watch(apiServiceProvider);
  return await apiService.getMeeting(meetingId);
});

final apiServiceProvider = Provider((ref) => ApiService());

class MeetingDetailScreen extends ConsumerWidget {
  final int meetingId;

  const MeetingDetailScreen({super.key, required this.meetingId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final meetingAsync = ref.watch(meetingProvider(meetingId));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Meeting Details'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              ref.refresh(meetingProvider(meetingId));
            },
          ),
        ],
      ),
      body: meetingAsync.when(
        data: (meeting) => _MeetingDetailBody(meeting: meeting),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 64, color: Colors.red),
              const SizedBox(height: 16),
              Text('Error: $error'),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  ref.refresh(meetingProvider(meetingId));
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MeetingDetailBody extends StatelessWidget {
  final Meeting meeting;

  const _MeetingDetailBody({required this.meeting});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          meeting.title,
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                      ),
                      _StatusBadge(status: meeting.status),
                    ],
                  ),
                  if (meeting.description != null && meeting.description!.isNotEmpty) ...[
                    const SizedBox(height: 8),
                    Text(
                      meeting.description!,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: Colors.grey,
                          ),
                    ),
                  ],
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Icon(Icons.access_time, size: 16, color: Colors.grey[600]),
                      const SizedBox(width: 4),
                      Text('Duration: ${meeting.formattedDuration}'),
                      const SizedBox(width: 16),
                      Icon(Icons.language, size: 16, color: Colors.grey[600]),
                      const SizedBox(width: 4),
                      Text(meeting.detectedLanguage?.toUpperCase() ?? 'Unknown'),
                      const SizedBox(width: 16),
                      Icon(Icons.smart_toy, size: 16, color: Colors.grey[600]),
                      const SizedBox(width: 4),
                      Text(meeting.modelUsed ?? 'Unknown'),
                    ],
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Summary Section
          if (meeting.summary != null && meeting.summary!.isNotEmpty) ...[
            _SectionCard(
              title: 'Summary',
              icon: Icons.summarize,
              child: Text(meeting.summary!),
            ),
            const SizedBox(height: 16),
          ],

          // Action Items
          if (meeting.actionItems != null && meeting.actionItems!.isNotEmpty) ...[
            _SectionCard(
              title: 'Action Items',
              icon: Icons.check_box,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: meeting.actionItems!
                    .map(
                      (item) => Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Icon(Icons.check_circle_outline, size: 20),
                            const SizedBox(width: 8),
                            Expanded(child: Text(item)),
                          ],
                        ),
                      ),
                    )
                    .toList(),
              ),
            ),
            const SizedBox(height: 16),
          ],

          // Key Points
          if (meeting.keyPoints != null && meeting.keyPoints!.isNotEmpty) ...[
            _SectionCard(
              title: 'Key Discussion Points',
              icon: Icons.lightbulb,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: meeting.keyPoints!
                    .map(
                      (point) => Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Icon(Icons.circle, size: 8),
                            const SizedBox(width: 8),
                            Expanded(child: Text(point)),
                          ],
                        ),
                      ),
                    )
                    .toList(),
              ),
            ),
            const SizedBox(height: 16),
          ],

          // Transcription
          if (meeting.transcription != null && meeting.transcription!.isNotEmpty) ...[
            _SectionCard(
              title: 'Full Transcription',
              icon: Icons.text_fields,
              actions: [
                IconButton(
                  icon: const Icon(Icons.copy),
                  onPressed: () {
                    Clipboard.setData(ClipboardData(text: meeting.transcription!));
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Transcription copied to clipboard')),
                    );
                  },
                  tooltip: 'Copy transcription',
                ),
              ],
              child: meeting.transcriptionSegments != null &&
                      meeting.transcriptionSegments!.isNotEmpty
                  ? Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: meeting.transcriptionSegments!
                          .map(
                            (segment) => Padding(
                              padding: const EdgeInsets.only(bottom: 12),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    segment.timeRange,
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: Colors.grey[600],
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(segment.text),
                                ],
                              ),
                            ),
                          )
                          .toList(),
                    )
                  : Text(meeting.transcription!),
            ),
          ],

          // Error message if failed
          if (meeting.isFailed && meeting.errorMessage != null) ...[
            Card(
              color: Colors.red[50],
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    const Icon(Icons.error, color: Colors.red),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Processing Failed',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.red,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(meeting.errorMessage!),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final Widget child;
  final List<Widget>? actions;

  const _SectionCard({
    required this.title,
    required this.icon,
    required this.child,
    this.actions,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, size: 24),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    title,
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ),
                if (actions != null) ...actions!,
              ],
            ),
            const Divider(height: 24),
            child,
          ],
        ),
      ),
    );
  }
}

class _StatusBadge extends StatelessWidget {
  final String status;

  const _StatusBadge({required this.status});

  @override
  Widget build(BuildContext context) {
    Color color;
    IconData icon;
    String label;

    switch (status) {
      case 'processing':
        color = Colors.orange;
        icon = Icons.hourglass_empty;
        label = 'Processing';
        break;
      case 'completed':
        color = Colors.green;
        icon = Icons.check_circle;
        label = 'Completed';
        break;
      case 'failed':
        color = Colors.red;
        icon = Icons.error;
        label = 'Failed';
        break;
      default:
        color = Colors.grey;
        icon = Icons.info;
        label = 'Uploaded';
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: color),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 12,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
