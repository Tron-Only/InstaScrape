import { useState } from "react";
import { Input } from "./components/ui/input";
import { Search } from "lucide-react";
import { Button } from "./components/ui/button";
import { SearchX } from "lucide-react";
import {
	Table,
	TableBody,
	TableCaption,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";
import mockdata from "@/lib/mockdata.json";

export default function App() {
	const [niche, setNiche] = useState("");
	const [active, setActive] = useState(false);

	return (
		<div className="min-h-screen bg-gray-50 px-4 py-12">
			<div className="flex items-center justify-center gap-2 mb-12">
				<Input
					type="text"
					placeholder="Look for a niche"
					className="transition-all ease-in duration-300 w-[240px] px-3 focus:w-[340px] hover:w-[340px]"
					value={niche}
					onChange={(e) => !active && setNiche(e.target.value)}
					disabled={active}
					onKeyDown={(e) => e.key === "Enter" && setActive(true)}
				/>
				<Button
					variant="ghost"
					className="p-2 hover:bg-gray-200 rounded-full"
					onClick={() => setActive((prev) => !prev)}
				>
					{active ? (
						<SearchX className="w-5 h-5 text-red-700" />
					) : (
						<Search className="w-5 h-5 text-gray-700" />
					)}
				</Button>
			</div>

			{active && (
				<div className="max-w-4xl mx-auto bg-white shadow-lg rounded-lg p-6 border">
					<Table>
						<TableCaption className="text-gray-600 italic mb-4">
							A list of all profiles with the word "{niche}"
						</TableCaption>
						<TableHeader>
							<TableRow className="bg-gray-100">
								<TableHead className="text-left text-sm font-medium text-gray-700">
									Name
								</TableHead>
								<TableHead className="text-left text-sm font-medium text-gray-700">
									Followers
								</TableHead>
							</TableRow>
						</TableHeader>
						<TableBody>
							{mockdata.map((profile, index) => (
								<TableRow key={index} className="hover:bg-gray-50">
									<TableCell className="text-sm text-blue-600 hover:underline">
										<a
											href={profile.link}
											target="_blank"
											rel="noopener noreferrer"
										>
											{profile.name}
										</a>
									</TableCell>
									<TableCell className="text-sm text-gray-800">
										{profile.followers.toLocaleString()}
									</TableCell>
								</TableRow>
							))}
						</TableBody>
					</Table>
				</div>
			)}
		</div>
	);
}
