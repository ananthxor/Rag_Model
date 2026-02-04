import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:rag_client/services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _controller = TextEditingController();
  final RagService _api = RagService();
  final List<ConsoleMessage> _messages = [];
  bool _isLoading = false;

  void _addMessage(String text, bool isUser) {
    setState(() {
      _messages.add(ConsoleMessage(text: text, isUser: isUser));
    });
  }

  Future<void> _handleSend() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    _addMessage(text, true);
    _controller.clear();
    setState(() => _isLoading = true);

    final answer = await _api.askQuestion(text);
    
    _addMessage(answer, false);
    setState(() => _isLoading = false);
  }

  Future<void> _handleUpload() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'txt'],
    );

    if (result != null) {
      final file = result.files.single;
      setState(() => _isLoading = true);
      _addMessage("Uploading ${file.name}...", false);
      
      final response = await _api.uploadDocument(file);
      
      _addMessage(response, false);
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      appBar: AppBar(
        title: const Text("Local RAG"),
        backgroundColor: Colors.transparent,
        actions: [
          IconButton(
            icon: const Icon(Icons.upload_file),
            onPressed: _handleUpload,
          )
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return Align(
                  alignment: msg.isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    margin: const EdgeInsets.only(bottom: 12),
                    constraints: const BoxConstraints(maxWidth: 600),
                    decoration: BoxDecoration(
                      color: msg.isUser 
                          ? Theme.of(context).colorScheme.primary.withOpacity(0.2)
                          : Theme.of(context).colorScheme.surface,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: Colors.white.withOpacity(0.1),
                      ),
                    ),
                    child: msg.isUser 
                      ? Text(msg.text, style: const TextStyle(color: Colors.white))
                      : MarkdownBody(data: msg.text, styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context))),
                  ),
                );
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: LinearProgressIndicator(),
            ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: "Ask about your docs...",
                      filled: true,
                      fillColor: Theme.of(context).colorScheme.surface,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(30),
                        borderSide: BorderSide.none,
                      ),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                    ),
                    onSubmitted: (_) => _handleSend(),
                  ),
                ),
                const SizedBox(width: 10),
                IconButton.filled(
                  onPressed: _handleSend, 
                  icon: const Icon(Icons.send)
                )
              ],
            ),
          )
        ],
      ),
    );
  }
}

class ConsoleMessage {
  final String text;
  final bool isUser;
  ConsoleMessage({required this.text, required this.isUser});
}
