// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';
import 'import.dart';

class ExampleModuleModel {
  String? s;
  int? n;
  ExampleModuleModel({
    this.s,
    this.n,
  });

  ExampleModuleModel copyWith({
    String? s,
    int? n,
  }) {
    return ExampleModuleModel(
      s: s ?? this.s,
      n: n ?? this.n,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      's': s,
      'n': n,
    };
  }

  factory ExampleModuleModel.fromMap(Map<String, dynamic> map) {
    return ExampleModuleModel(
      s: map['s'] != null ? map['s'] as String : null,
      n: map['n'] != null ? map['n'] as int : null,
    );
  }

  String toJson() => json.encode(toMap());

  factory ExampleModuleModel.fromJson(String source) => ExampleModuleModel.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'ExampleModuleModel(s: $s, n: $n)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
  
    return other is ExampleModuleModel &&
      other.s == s &&
      other.n == n;
  }

  @override
  int get hashCode => s.hashCode ^ n.hashCode;
}
