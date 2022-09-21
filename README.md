game.ReplicatedStorage.EventShop.Ak47Event.OnServerEvent:Connect(function(player)
	if player.leaderstats.Cash.Value >= 100 then 
		player.leaderstats.Cash.Value = player.leaderstats.Cash.Value - 100
		game.ServerStorage.Tools.Ak:Clone().Parent = player.Backpack
	end	
end)
