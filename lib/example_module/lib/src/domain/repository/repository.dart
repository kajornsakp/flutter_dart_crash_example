import '../models/index.dart';

abstract class ExampleModuleRepository {
  const ExampleModuleRepository();

  ExampleModuleModel generateRandomModel();
}