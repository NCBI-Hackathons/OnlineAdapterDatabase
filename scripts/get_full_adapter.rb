sam = File.open("fixed_truseq_part.csv","w")
File.open("TruSeq_part.csv","r") do |file|
	file.each_line do |line|
		array = line.split(",")
		full_seq1 = array[2].gsub("[i7]","#{array[0]}")
		full_seq2 = full_seq1.gsub("[i5]","#{array[0]}")
		sam.puts full_seq2
	end
end
