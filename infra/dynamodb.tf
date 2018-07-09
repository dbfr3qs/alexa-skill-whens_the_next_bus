resource "aws_dynamodb_table" "userid-dynamodb-table" {
  name           = "UserIDBusStop"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }

//   attribute {
//     name = "BusStop"
//     type = "N"
//   }

  ttl {
    attribute_name = "TimeToExist"
    enabled = false
  }

//   tags {
//     Name        = "dynamodb-table-1"
//     Environment = "production"
//   }
}