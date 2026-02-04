import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';

class RagService {
  // Use 10.0.2.2 for Android Emulator to access localhost
  // Use 127.0.0.1 for iOS/Desktop
  // Allow passing the URL via --dart-define=API_URL=...
  static const String _envUrl = String.fromEnvironment('API_URL');
  static const String _defaultUrl = "http://127.0.0.1:8000";

  String getBaseUrl() {
    // If an environment variable is provided, strictly use it.
    if (_envUrl.isNotEmpty) return _envUrl;
    
    // Otherwise fallback to platform-specific defaults
    if (Platform.isAndroid) return "http://10.0.2.2:8000";
    return _defaultUrl;
  }

  Future<Map<String, dynamic>> checkHealth() async {
    try {
      final response = await http.get(Uri.parse('${getBaseUrl()}/health'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      throw Exception('Failed to connect to server');
    } catch (e) {
      throw Exception('Server error: $e');
    }
  }

  Future<String> askQuestion(String query) async {
    try {
      final response = await http.post(
        Uri.parse('${getBaseUrl()}/ask/?query=$query'),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['answer'] ?? "No answer received.";
      } else {
        throw Exception("Error: ${response.statusCode}");
      }
    } catch (e) {
      return "Failed to get answer: $e";
    }
  }

  Future<String> uploadDocument(PlatformFile file) async {
    var uri = Uri.parse('${getBaseUrl()}/ingest/');
    var request = http.MultipartRequest('POST', uri);
    
    // Handle Web vs Native file access
    if (file.bytes != null) {
      request.files.add(http.MultipartFile.fromBytes(
        'file', 
        file.bytes!, 
        filename: file.name
      ));
    } else if (file.path != null) {
       request.files.add(await http.MultipartFile.fromPath(
        'file', 
        file.path!
      ));     
    }

    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        return "Upload successful: ${file.name}";
      } else {
        return "Upload failed: ${response.statusCode}";
      }
    } catch (e) {
      return "Upload error: $e";
    }
  }
}
