ir = r'''
@.str = private unnamed_addr constant [5 x i8] c"%ld\0A\00", align 1

declare dso_local i32 @printf(i8*, ...)

define dso_local i64 @print(i64 %0) {
  %2 = alloca i64, align 8
  store i64 %0, i64* %2, align 8
  %3 = load i64, i64* %2, align 8
  %4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str, i64 0, i64 0), i64 %3)
  %5 = sext i32 %4 to i64
  ret i64 %5
}
'''