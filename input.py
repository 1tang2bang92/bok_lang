ir = r'''
@.str = private unnamed_addr constant [4 x i8] c"%ld\00", align 1

define dso_local i64 @input() local_unnamed_addr {
  %1 = alloca i64, align 8
  %2 = bitcast i64* %1 to i8*
  %3 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i64 0, i64 0), i64* nonnull %1)
  %4 = load i64, i64* %1, align 8
  ret i64 %4
}

declare dso_local i32 @scanf(i8* nocapture readonly, ...) local_unnamed_addr
'''